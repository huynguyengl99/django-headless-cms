from headless_cms.admin import auto_admins
from headless_cms.contrib.astrowind.astrowind_posts.models import (
    AWCategory,
    AWPost,
    AWPostImage,
    AWPostTag,
)

auto_admins(
    [
        AWPostTag,
        AWCategory,
        AWPostImage,
        AWPost,
    ]
)
