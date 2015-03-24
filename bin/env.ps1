param (
    [Hashtable]$vars,
    [ScriptBlock]$sb
)

$oldenv = @{}
foreach ($k in $vars.Keys) {
    $oldenv[$k] = (Get-Item -ea 0 env:$k)
}
try {
    foreach ($k in $vars.Keys) {
        Set-Item -ea 0 env:$k $vars[$k]
    }
    &$sb
}
finally {
    foreach ($k in $oldenv.Keys) {
        Set-Item -ea 0 env:$k $oldenv[$k]
    }
}
