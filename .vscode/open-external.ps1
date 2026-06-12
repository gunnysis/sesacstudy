# 현재 파일을 OS 기본 앱(브라우저/PDF 뷰어 등)으로 연다.
# study_docs_link(공유 강의자료)는 수시로 재구성되어 VSCode 가 들고 있는 경로가
# 죽는(stale) 경우가 잦다. 경로가 없으면 같은 파일명을 현재 트리에서 찾아 자가 치유한다.
param([Parameter(Mandatory = $true)][string]$Path)

$ErrorActionPreference = 'Stop'
$root = Join-Path $PSScriptRoot '..\study_docs_link'

# 1) 경로가 그대로 살아 있으면 바로 연다.
if (Test-Path -LiteralPath $Path) {
    Start-Process -FilePath $Path
    return
}

# 2) 이동·재구성됐을 수 있으니 같은 파일명을 현재 트리에서 검색한다.
#    (한글 경로는 NFC/NFD 정규화 차이로 단순 비교가 어긋날 수 있어 FormC 로 정규화해 비교)
if (Test-Path -LiteralPath $root) {
    $leaf = (Split-Path -Path $Path -Leaf).Normalize([Text.NormalizationForm]::FormC)
    $hit = Get-ChildItem -LiteralPath $root -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $_.Name.Normalize([Text.NormalizationForm]::FormC) -eq $leaf } |
        Select-Object -First 1
    if ($hit) {
        Start-Process -FilePath $hit.FullName
        Write-Host "이동된 파일을 찾아 열었습니다: $($hit.FullName)"
        return
    }
    # 3) 못 찾으면 현재 트리를 탐색기로 열어 직접 찾게 한다.
    Write-Warning "원래 경로가 없고 같은 이름의 파일도 못 찾았습니다. 탐색기를 엽니다."
    Start-Process explorer.exe (Resolve-Path -LiteralPath $root).Path
    return
}

throw "경로를 찾을 수 없습니다: $Path"
