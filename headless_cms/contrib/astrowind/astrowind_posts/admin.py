from headless_cms.admin import auto_admins
from headless_cms.contrib.astrowind.astrowind_posts.models import (
    AWCategory,
    AWPost,
    AWPostImage,
    AWPostMetadata,
    AWPostTag,
)

auto_admins(
    [
        AWPostMetadata,
        AWPostTag,
        AWCategory,
        AWPostImage,
        AWPost,
    ]
)
