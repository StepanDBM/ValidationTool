using System;
using System.Windows.Input;

namespace ValidationTool.UI.Commands {
    public class RelayCommand : ICommand {
        private readonly Action _execute;
        /// <summary>
        /// Initializes a new instance of the <see cref="RelayCommand"/> class.
        /// </summary>
        /// <param name="execute">The action to execute.</param>
        public RelayCommand(Action execute) {
            _execute = execute;
        }

        public event EventHandler CanExecuteChanged;

        public bool CanExecute(object parameter) => true;

        public void Execute(object parameter) {
            System.Diagnostics.Debug.WriteLine("BUTTON FIRED");
            _execute();
        }
    }
}