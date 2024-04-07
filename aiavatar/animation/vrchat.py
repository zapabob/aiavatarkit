import asyncio
from time import time
from pythonosc import udp_client
from . import AnimationControllerBase


class VRChatAnimationController(AnimationControllerBase):
    def __init__(self, osc_address: str="/avatar/parameters/VRCEmote", animations: dict=None, idling_key: str="idling", host: str="127.0.0.1", port: int=9000, verbose: bool=False):
        super().__init__(animations=animations, idling_key=idling_key, verbose=verbose)

        self.osc_address = osc_address
        self.host = host
        self.port = port
        self.client = udp_client.SimpleUDPClient(self.host, self.port)

    async def animate(self, name: str, duration: float):
        self.subscribe_reset(time() + duration)

        osc_value = self.faces.get(name)
        if osc_value is None:
            self.logger.warning(f"Animation '{name}' is not registered")
            return

        self.logger.info(f"animation: {name} ({osc_value})")
        self.client.send_message(self.osc_address, osc_value)

    def test_osc(self):
        while True:
            self.animate(input("Animation name: "), 3.0)


if __name__ == "__main__":
    vrc_animation_controller = VRChatAnimationController()
    asyncio.run(vrc_animation_controller.test_osc())
