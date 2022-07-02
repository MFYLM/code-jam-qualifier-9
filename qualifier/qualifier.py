import typing
from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Request:
    scope: typing.Mapping[str, typing.Any]                      # Mapping object defines __getitem__ ("[]" operation), __len__, __iter__ ("iter()" method)
    receive: typing.Callable[[], typing.Awaitable[object]]
    send: typing.Callable[[object], typing.Awaitable[None]]


class RestaurantManager:
    def __init__(self):
        """Instantiate the restaurant manager.

        This is called at the start of each day before any staff get on
        duty or any orders come in. You should do any setup necessary
        to get the system working before the day starts here; we have
        already defined a staff dictionary.
        """
        self.staff = {}

    async def __call__(self, request: Request):
        """Handle a request received.

        This is called for each request received by your application.
        In here is where most of the code for your system should go.

        :param request: request object
            Request object containing information about the sent
            request to your application.
        """
        if request.scope["type"] == "staff.onduty":
            self.staff[request.scope["id"]] = request
        elif request.scope["type"] == "staff.offduty":
            if request.scope["id"] in self.staff:
                del self.staff[request.scope["id"]]
        elif request.scope["type"] == "order":
            founds = []

            for k, r in self.staff.items():
                if type(r.scope["speciality"]) == str and r.scope["speciality"] == request.scope["speciality"]:
                    founds.append(self.staff[k])
                elif request.scope["speciality"] in r.scope["speciality"]:
                    founds.append(self.staff[k])

            index = random.randint(0, len(founds) - 1)
            found = founds[index]
            full_order = await request.receive()
            await found.send(full_order)

            result = await found.receive()
            await request.send(result)
        