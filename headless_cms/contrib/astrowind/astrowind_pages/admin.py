from headless_cms.admin import auto_admins
from headless_cms.contrib.astrowind.astrowind_pages.models import (
    AWAboutPage,
    AWContactPage,
    AWIndexPage,
    AWPostPage,
    AWPricingPage,
    AWSite,
)

auto_admins(
    [
        AWAboutPage,
        AWContactPage,
        AWIndexPage,
        AWPricingPage,
        AWPostPage,
        AWSite,
    ]
)
