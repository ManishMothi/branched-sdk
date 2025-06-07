import datetime
from collections.abc import Mapping
from typing import Any, TypeVar, Union, cast
from uuid import UUID

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

from ..types import UNSET, Unset

T = TypeVar("T", bound="TreeNodeRead")


@_attrs_define
class TreeNodeRead:
    """
    Attributes:
        id (UUID):
        chat_session_id (UUID):
        parent_id (Union[None, UUID]):
        user_message (str):
        llm_response (str):
        created_at (datetime.datetime):
        children (Union[Unset, list['TreeNodeRead']]):
    """

    id: UUID
    chat_session_id: UUID
    parent_id: Union[None, UUID]
    user_message: str
    llm_response: str
    created_at: datetime.datetime
    children: Union[Unset, list["TreeNodeRead"]] = UNSET
    additional_properties: dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> dict[str, Any]:
        id = str(self.id)

        chat_session_id = str(self.chat_session_id)

        parent_id: Union[None, str]
        if isinstance(self.parent_id, UUID):
            parent_id = str(self.parent_id)
        else:
            parent_id = self.parent_id

        user_message = self.user_message

        llm_response = self.llm_response

        created_at = self.created_at.isoformat()

        children: Union[Unset, list[dict[str, Any]]] = UNSET
        if not isinstance(self.children, Unset):
            children = []
            for children_item_data in self.children:
                children_item = children_item_data.to_dict()
                children.append(children_item)

        field_dict: dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "id": id,
                "chat_session_id": chat_session_id,
                "parent_id": parent_id,
                "user_message": user_message,
                "llm_response": llm_response,
                "created_at": created_at,
            }
        )
        if children is not UNSET:
            field_dict["children"] = children

        return field_dict

    @classmethod
    def from_dict(cls: type[T], src_dict: Mapping[str, Any]) -> T:
        d = dict(src_dict)
        id = UUID(d.pop("id"))

        chat_session_id = UUID(d.pop("chat_session_id"))

        def _parse_parent_id(data: object) -> Union[None, UUID]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                parent_id_type_0 = UUID(data)

                return parent_id_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, UUID], data)

        parent_id = _parse_parent_id(d.pop("parent_id"))

        user_message = d.pop("user_message")

        llm_response = d.pop("llm_response")

        created_at = isoparse(d.pop("created_at"))

        children = []
        _children = d.pop("children", UNSET)
        for children_item_data in _children or []:
            children_item = TreeNodeRead.from_dict(children_item_data)

            children.append(children_item)

        tree_node_read = cls(
            id=id,
            chat_session_id=chat_session_id,
            parent_id=parent_id,
            user_message=user_message,
            llm_response=llm_response,
            created_at=created_at,
            children=children,
        )

        tree_node_read.additional_properties = d
        return tree_node_read

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
