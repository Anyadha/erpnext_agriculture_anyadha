import frappe
from frappe import _
from frappe.model.document import Document


class JuteGrowerRegistration(Document):

	def validate(self):
		self.validate_aadhaar()
		self.validate_mobile()
		self.validate_consent()
		self.validate_yield()
		self.sync_consent_farmer_name()

	def on_submit(self):
		self.check_mandatory_consent()

	def validate_aadhaar(self):
		aadhaar = (self.aadhaar_number or "").replace("-", "").replace(" ", "")
		if aadhaar and len(aadhaar) != 12:
			frappe.throw(
				_("Aadhaar Number must be 12 digits (masked or full). Got {0} characters.").format(len(aadhaar))
			)

	def validate_mobile(self):
		mobile = (self.mobile_number or "").strip()
		if mobile and (not mobile.isdigit() or len(mobile) != 10):
			frappe.throw(_("Mobile Number must be exactly 10 digits."))

	def validate_consent(self):
		if self.consent_given and not self.consent_date:
			frappe.throw(_("Please enter the Consent Date when consent is given."))

	def validate_yield(self):
		if self.was_jute_cultivated_last_year == "No" and self.yield_per_bigha_last_year:
			frappe.msgprint(
				_("Yield per Bigha is filled but 'Was Jute Cultivated Last Year?' is set to No. Please verify."),
				alert=True,
				indicator="orange",
			)
		if self.total_land_bighas_this_year and self.total_land_bighas_this_year <= 0:
			frappe.throw(_("Total Land (Bighas) must be a positive value."))

	def sync_consent_farmer_name(self):
		if not self.consent_farmer_name and self.farmer_name:
			self.consent_farmer_name = self.farmer_name

	def check_mandatory_consent(self):
		if not self.consent_given:
			frappe.throw(
				_("Cannot submit without farmer consent. Please tick 'Consent Given' before submitting.")
			)
