using System.ComponentModel;

namespace ValidationTool.UI.Models.DTOs {
    public class SelectionContext : INotifyPropertyChanged {
        private string _selectedTeam;
        public string SelectedTeam {
            get => _selectedTeam;
            set {
                if (_selectedTeam != value) {
                    _selectedTeam = value;
                    SelectedArtist = null;
                    SelectedFile = null;
                    OnPropertyChanged(nameof(SelectedTeam));
                }
            }
        }

        private string _selectedArtist;
        public string SelectedArtist {
            get => _selectedArtist;
            set {
                if (_selectedArtist != value) {
                    _selectedArtist = value;
                    SelectedFile = null;
                    OnPropertyChanged(nameof(SelectedArtist));
                }
            }
        }

        private string _selectedFile;
        public string SelectedFile {
            get => _selectedFile;
            set {
                if (_selectedFile != value) {
                    _selectedFile = value;
                    OnPropertyChanged(nameof(SelectedFile));
                }
            }
        }

        public event PropertyChangedEventHandler PropertyChanged;

        private void OnPropertyChanged(string name) {
            PropertyChanged?.Invoke(this, new PropertyChangedEventArgs(name));
        }
    }

}