from typing import Dict

from typing_extensions import TypedDict

from checkov.cloudformation.graph_builder.graph_components.block_types import CloudformationTemplateSections, BlockType
from checkov.cloudformation.graph_builder.graph_components.blocks import CloudformationBlock
from checkov.common.graph.graph_builder.local_graph import LocalGraph


class Undetermined(TypedDict):
    module_vertex_id: int
    attribute_name: str
    variable_vertex_id: int


class CloudformationLocalGraph(LocalGraph):
    def __init__(self, cfn_definitions: Dict, source="CloudFormation") -> None:
        super().__init__()
        self.definitions = cfn_definitions
        self.source = source

    def build_graph(self, render_variables: bool) -> None:
        self._create_vertices()

    def _create_vertices(self) -> None:
        for file_path, file_conf in self.definitions.items():
            self._create_resources_vertices(file_path, get_only_dict_items(file_conf.get(CloudformationTemplateSections.RESOURCES.value, [])))

    def _create_resources_vertices(self, file_path, resources):
        for resource_name, resource in resources.items():
            resource = resources[resource_name]
            resource_type = resource.get("Type")
            attributes = resource.get("Properties")
            attributes["resource_type"] = resource_type
            block = CloudformationBlock(name=".".join([resource_type, resource_name]),
                                        config=resource.get("Properties"),
                                        path=file_path,
                                        block_type=BlockType.RESOURCE,
                                        attributes=attributes,
                                        id=".".join([resource_type, resource_name]),
                                        source=self.source
                                        )
            self.vertices.append(block)


def get_only_dict_items(origin_dict: Dict) -> Dict:
    return {key: origin_dict[key] for key in origin_dict.keys() if isinstance(origin_dict[key], dict)}
