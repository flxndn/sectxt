" Vim syntax file
" Language:     SEC Sections Document
:syntax region Comment start="#" end="$"
:syntax region Underlined start="\[\[" end="\]\]"
:syntax region MoreMsg start="#" end="$"
:syntax region Special start="* " end="$"
:syntax region ModeMsg start="-" end="$"
:syntax region Identifier start=">" end="$"
