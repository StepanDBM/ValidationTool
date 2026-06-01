namespace ValidationTool.UI.Models.Config {
    public class MeshBudgetModel {
        public int MaxVertices { get; set; }
        public int MaxTriangles { get; set; }
        public int MaxMaterialSlots { get; set; }
    }

    public class BudgetsConfigModel {
        public MeshBudgetModel StaticMesh { get; set; } = new MeshBudgetModel();
        public MeshBudgetModel Character { get; set; } = new MeshBudgetModel();
        public MeshBudgetModel Weapon { get; set; } = new MeshBudgetModel();
        public MeshBudgetModel Prop { get; set; } = new MeshBudgetModel();
        public MeshBudgetModel Environment { get; set; } = new MeshBudgetModel();
    }
}