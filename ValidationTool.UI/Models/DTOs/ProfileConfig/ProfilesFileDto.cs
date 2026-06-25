using System.Collections.Generic;

namespace ValidationTool.UI.Models.DTOs.Profiles {
    public class ProfilesFileDto {
        public List<ProfileDto> profiles { get; set; } = new List<ProfileDto>();
    }
}