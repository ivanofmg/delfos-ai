# =========================
# DELFOS FIX SCRIPT (CORE REFACTOR)
# =========================

Write-Host "=== INICIANDO FIX CORE REFACTOR ==="

# 1. Crear __init__.py (si no existen)
$paths = @(
    "core",
    "core\graph",
    "core\simulation",
    "core\agents",
    "core\economics",
    "core\prompts",
    "core\schemas",
    "core\domain"
)

foreach ($p in $paths) {
    $file = "$p\__init__.py"
    if (-not (Test-Path $file)) {
        New-Item $file -ItemType File | Out-Null
        Write-Host "✔ Created $file"
    }
}

# 2. Fix imports en graph.py
$graphFile = "backend\app\api\graph.py"

(Get-Content $graphFile) `
-replace "\.\.services\.ontology_generator", "core.graph.ontology_generator" `
-replace "\.\.services\.graph_builder", "core.graph.graph_builder" `
-replace "\.\.services\.zep_entity_reader", "core.graph.zep_entity_reader" `
| Set-Content $graphFile

Write-Host "✔ graph.py imports fixed"

# 3. Fix imports en simulation.py
$simFile = "backend\app\api\simulation.py"

(Get-Content $simFile) `
-replace "\.\.services\.zep_entity_reader", "core.graph.zep_entity_reader" `
-replace "\.\.services\.oasis_profile_generator", "core.agents.oasis_profile_generator" `
-replace "\.\.services\.simulation_manager", "core.simulation.simulation_manager" `
-replace "\.\.services\.simulation_runner", "core.simulation.simulation_runner" `
| Set-Content $simFile

Write-Host "✔ simulation.py imports fixed"

# 4. Validar estructura core
Write-Host "`n=== VALIDANDO ESTRUCTURA ==="
Get-ChildItem core -Recurse -Depth 2 | Select FullName

# 5. Verificar Python import path
Write-Host "`n=== TEST IMPORTS ==="

$test = @"
import sys
sys.path.append('.')

try:
    from core.graph.graph_builder import GraphBuilderService
    from core.simulation.simulation_manager import SimulationManager
    from core.agents.oasis_profile_generator import OasisProfileGenerator
    print("OK_IMPORTS")
except Exception as e:
    print("IMPORT_ERROR:", e)
"@

$test | Out-File test_imports.py -Encoding utf8
python test_imports.py
Remove-Item test_imports.py

# 6. FIX GIT PATH (si no reconoce git)
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "`n⚠ Git no está en PATH. Intentando fix..."

    $gitPaths = @(
        "C:\Program Files\Git\cmd",
        "C:\Program Files\Git\bin"
    )

    foreach ($gp in $gitPaths) {
        if (Test-Path $gp) {
            $env:Path += ";$gp"
            Write-Host "✔ Added $gp to PATH"
        }
    }
}

# 7. Test git
if (Get-Command git -ErrorAction SilentlyContinue) {
    git --version
} else {
    Write-Host "❌ Git sigue sin estar disponible (reinicia terminal)"
}

Write-Host "`n=== LISTO ==="
Write-Host "Ahora ejecuta:"
Write-Host "cd backend"
Write-Host "python run.py"