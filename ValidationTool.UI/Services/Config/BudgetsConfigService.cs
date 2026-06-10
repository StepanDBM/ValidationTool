using System.IO;
using System.Text.Json;
using ValidationTool.UI.Models.Config;
using ValidationTool.UI.Services.Config;

namespace ValidationTool.UI.Services.Config {
    public class BudgetsConfigService {
        private static readonly string budgetPath = Path.Combine(Paths.GEN_CONFIGS.ToString(), "budgets.json");

        public BudgetsConfigModel Load() {
            if (!File.Exists(budgetPath))
                return CreateDefault();

            var json = File.ReadAllText(budgetPath);

            var config = JsonSerializer.Deserialize<BudgetsConfigModel>(json,
                new JsonSerializerOptions {
                    PropertyNameCaseInsensitive = true
                });

            return Repair(config);
        }

        public void Save(BudgetsConfigModel config) {
            var json = JsonSerializer.Serialize(config, new JsonSerializerOptions {
                WriteIndented = true
            });

            File.WriteAllText(budgetPath, json);
        }

        private BudgetsConfigModel Repair(BudgetsConfigModel c) {
            if (c == null)
                return CreateDefault();

            if (c.StaticMesh == null)
                c.StaticMesh = new MeshBudgetModel();

            if (c.Character == null)
                c.Character = new MeshBudgetModel();

            if (c.Weapon == null)
                c.Weapon = new MeshBudgetModel();

            if (c.Prop == null)
                c.Prop = new MeshBudgetModel();

            if (c.Environment == null)
                c.Environment = new MeshBudgetModel();

            return c;
        }

        private BudgetsConfigModel CreateDefault() {
            return new BudgetsConfigModel {
                StaticMesh = new MeshBudgetModel(),
                Character = new MeshBudgetModel(),
                Weapon = new MeshBudgetModel(),
                Prop = new MeshBudgetModel(),
                Environment = new MeshBudgetModel()
            };
        }
    }
}