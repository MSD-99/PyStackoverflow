from types import SimpleNamespace

from src.utils.keyboard import Create_Keyboard

Keys = SimpleNamespace(
    settings = ':gear: Settings',
)


Keyboards = SimpleNamespace(
    main = Create_Keyboard(Keys.settings),
)

States = SimpleNamespace(
    main="MAIN",
)
