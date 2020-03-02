from checkov.terraform.checks.resource.BaseResourceValueCheck import BaseResourceValueCheck
from checkov.terraform.models.enums import CheckCategories


class EBSSnapshotEncryption(BaseResourceValueCheck):
    def __init__(self):
        name = "Ensure all data stored in the EBS Snapshot is securely encrypted "
        id = "CKV_AWS_4"
        supported_resources = ['aws_ebs_snapshot']
        categories = [CheckCategories.ENCRYPTION]
        super().__init__(name=name, id=id, categories=categories, supported_resources=supported_resources)

    def get_inspected_key(self):
        return "encrypted"


check = EBSSnapshotEncryption()
