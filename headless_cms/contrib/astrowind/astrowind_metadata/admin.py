from headless_cms.admin import auto_admins
from headless_cms.contrib.astrowind.astrowind_metadata.models import (
    AWMetadata,
    AWMetadataImage,
    AWMetaDataOpenGraph,
    AWMetadataRobot,
    AWMetaDataTwitter,
)

auto_admins(
    [
        AWMetadataRobot,
        AWMetadataImage,
        AWMetaDataOpenGraph,
        AWMetaDataTwitter,
        AWMetadata,
    ]
)
