using System.Collections.Generic;
using ValidationTool.UI.MVVM;

namespace ValidationTool.UI.Models.Config {
    public class NamingRulesModel : ObservableObject {
        public List<string> ValidPrefixes { get; set; } = new List<string>();
        public List<string> DefaultMayaNames { get; set; } = new List<string>();

        private string _namePattern;
        public string NamePattern {
            get { return _namePattern; }
            set { Set(ref _namePattern, value); }
        }
    }
}