for /l %%i in (1 1 35) do start call call python update_stock_data.py all_stock_code_list.txt %%i00 100
pause