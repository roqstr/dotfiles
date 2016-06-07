
syntax enable
set number
set background=dark
colorscheme vitamins 
execute pathogen#infect()
filetype plugin indent on
autocmd VimEnter * NERDTree
autocmd VimEnter * wincmd p 

set rtp+=/lib/python3.5/site-packages/powerline/bindings/vim/
set laststatus=2
set showtabline=2 
set noshowmode
