"""
Fixtures for Agriculture App
Provides sample data and standard configuration
"""

fixtures = [
    {
        "dt": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Project-farm",
                    "Project-field",
                    "Project-crop_item",
                    "Project-season",
                    "Project-area_under_cultivation",
                    "Project-expected_yield_per_unit",
                    "Project-expected_total_yield",
                    "Project-actual_yield",
                    "Project-total_costing_amount",
                    "Project-total_sales_amount",
                    "Stock Entry-farm",
                    "Stock Entry-field",
                    "Stock Entry-operation_type",
                    "Stock Entry-harvest_record",
                    "Timesheet-farm",
                    "Timesheet-field",
                    "Timesheet-operation_log",
                    "Asset-farm",
                    "Asset-asset_category",
                    "Employee-primary_farm",
                    "Employee-agriculture_role"
                ]
            ]
        ]
    },
    {
        "dt": "Role",
        "filters": [
            [
                "name",
                "in",
                [
                    "Agriculture Manager",
                    "Agriculture User"
                ]
            ]
        ]
    }
]
