vim9script

# run the main python file
nnoremap <leader>m :update<CR>:ScratchTermReplaceU .venv/Scripts/python.exe src/ascii_image/main.py<CR>
nnoremap <leader>l :call g:RunPrecommit()<CR>
nnoremap <leader>L :call g:RunPrecommitAll()<CR>
