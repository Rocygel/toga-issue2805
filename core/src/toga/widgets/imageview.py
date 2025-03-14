from __future__ import annotations

from typing import TYPE_CHECKING, Any, Literal

from travertino.size import at_least

import toga
from toga.style.pack import NONE
from toga.widgets.base import StyleT, Widget

if TYPE_CHECKING:
    from toga.images import ImageContentT, ImageT


def rehint_imageview(
    image: toga.Image,
    style: StyleT,
    scale: int = 1,
) -> tuple[int, int, float | None]:
    """Compute the size hints for an ImageView based on the image.

    This logic is common across all backends, so it's shared here.

    :param image: The image being displayed.
    :param style: The style object for the imageview.
    :param scale: The scale factor (if any) to apply to native pixel sizes.
    :returns: A triple containing the intrinsic width hint, intrinsic height hint, and
        the aspect ratio to preserve (or None if the aspect ratio should not be
        preserved).
    """
    if image:
        if style.width != NONE and style.height != NONE:
            # Explicit width and height for image. Scale the rendered image
            # to fit the explicitly provided size.
            width = int(style.width * scale)
            height = int(style.height * scale)
            aspect_ratio = None

        elif style.width != NONE:
            # Explicit width, implicit height. Preserve aspect ratio.
            aspect_ratio = image.width / image.height
            width = int(style.width * scale)
            height = int(style.width * scale / aspect_ratio)
            if style.flex:
                height = at_least(0)
        elif style.height != NONE:
            # Explicit height, implicit width. Preserve aspect ratio.
            aspect_ratio = image.width / image.height
            width = int(style.height * scale * aspect_ratio)
            height = int(style.height * scale)
            if style.flex:
                width = at_least(0)
        else:
            # Use the image's actual size.
            aspect_ratio = image.width / image.height
            width = int(image.width * scale)
            height = int(image.height * scale)
            if style.flex:
                width = at_least(0)
                height = at_least(0)
    else:
        # No image. Hinted size is 0.
        width = 0
        height = 0
        aspect_ratio = None

    return width, height, aspect_ratio


class ImageView(Widget):
    def __init__(
        self,
        image: ImageContentT | None = None,
        id: str | None = None,
        style: StyleT | None = None,
        **kwargs,
    ):
        """Create a new image view.

        :param image: The image to display. Can be any valid :any:`image content
            <ImageContentT>` type; or :any:`None` to display no image.
        :param id: The ID for the widget.
        :param style: A style object. If no style is provided, a default style will be
            applied to the widget.
        :param kwargs: Initial style properties.
        """
        # Prime the image attribute
        self._image = None

        super().__init__(id, style, **kwargs)

        self.image = image

    def _create(self) -> Any:
        return self.factory.ImageView(interface=self)

    @property
    def enabled(self) -> Literal[True]:
        """Is the widget currently enabled? i.e., can the user interact with the widget?

        ImageView widgets cannot be disabled; this property will always return True; any
        attempt to modify it will be ignored.
        """
        return True

    @enabled.setter
    def enabled(self, value: object) -> None:
        pass

    def focus(self) -> None:
        """No-op; ImageView cannot accept input focus."""
        pass

    @property
    def image(self) -> toga.Image | None:
        """The image to display.

        When setting an image, you can provide any valid :any:`image content
        <ImageContentT>` type; or :any:`None` to clear the image view.
        """
        return self._image

    @image.setter
    def image(self, image: ImageContentT) -> None:
        if isinstance(image, toga.Image):
            self._image = image
        elif image is None:
            self._image = None
        else:
            self._image = toga.Image(image)

        self._impl.set_image(self._image)
        self.refresh()

    def as_image(self, format: type[ImageT] = toga.Image) -> ImageT:
        """Return the image in the specified format.

        :param format: Format to provide. Defaults to :class:`~toga.images.Image`; also
            supports :any:`PIL.Image.Image` if Pillow is installed, as well as any image
            types defined by installed :doc:`image format plugins
            </reference/plugins/image_formats>`.
        :returns: The image in the specified format.
        """
        return self.image.as_format(format)
