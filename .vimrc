
syntax enable
set number
set background=dark
colorscheme skittles_dark
execute pathogen#infect()
filetype plugin indent on
autocmd VimEnter * NERDTree
autocmd VimEnter * wincmd p 
