from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, List, Optional

from vkwave.bots.dispatching.events.base import BaseEvent
from vkwave.bots.dispatching.filters.base import BaseFilter
from vkwave.bots.dispatching.filters.manage import FilterManager

from .callback import BaseCallback

FILTERS_NOT_PASSED = object()


class BaseHandler(ABC):
    filter_manager: FilterManager

    @abstractmethod
    def __init__(
            self, callback: BaseCallback, filters: Optional[List[BaseFilter]] = None
    ):
        ...

    @abstractmethod
    async def process_event(self, event: BaseEvent) -> Any:
        """Return FILTERS_NOT_PASSED or handler's result"""


class DefaultHandler(BaseHandler):
    def __init__(
            self, callback: BaseCallback, filters: Optional[List[BaseFilter]] = None
    ):
        self.callback = callback
        self.filter_manager = FilterManager()
        filters = filters or []
        for filter in filters:
            self.filter_manager.add_filter(filter)

    async def process_event(self, event: BaseEvent) -> Any:
        f_result = await self.filter_manager.execute_filters(event)
        if not f_result:
            return FILTERS_NOT_PASSED
        c_result = await self.callback.execute(event)
        return c_result