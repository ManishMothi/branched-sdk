import datetime
from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, TypeVar, Union
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

if TYPE_CHECKING:
    from ..models.tree_node_read import TreeNodeRead


T = TypeVar("T", bound="ChatSessionRead")


@_attrs_define
class ChatSessionRead:
    """
    Attributes:
        id (UUID):
        user_id (str):
        created_at (datetime.datetime):
        nodes (Union[Unset, list['TreeNodeRead']]): List of nodes in the session
    """

    id: UUID
    user_id: str
    created_at: datetime.datetime
    nodes: Union[Unset, list["TreeNodeRead"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        user_id = self.user_id

        created_at = self.created_at.isoformat()

        nodes: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.nodes, Unset):
            nodes = []
            for nodes_item_data in self.nodes:
                nodes_item = nodes_item_data.to_dict()
                nodes.append(nodes_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "user_id": user_id,
                "created_at": created_at,
            }
        )
        if nodes is not UNSET:
            field_dict["nodes"] = nodes

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        from ..models.tree_node_read import TreeNodeRead

        d = dict(src_dict)
        id = UUID(d.pop("id"))

        user_id = d.pop("user_id")

        created_at = isoparse(d.pop("created_at"))

        nodes = []
        _nodes = d.pop("nodes", UNSET)
        for nodes_item_data in _nodes or []:
            nodes_item = TreeNodeRead.from_dict(nodes_item_data)

            nodes.append(nodes_item)

        chat_session_read = cls(
            id=id,
            user_id=user_id,
            created_at=created_at,
            nodes=nodes,
        )

        chat_session_read.additional_properties = d
        return chat_session_read

    @property
    def additional_keys(self) -> list[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
