import os

# 获取交易的开始和结束时间
start_date = '2015-01-01'
end_date = '2022-10-15'

project_path = os.path.split(os.path.abspath(os.path.realpath(__file__)))[0] + "/.."

# 沪交所股票代码路径，深交所股票代码路径
sh_code_path = f'{project_path}/csvfile/sh_code.csv'
sz_code_path = f'{project_path}/csvfile/sz_code.csv'
all_code_path = f'{project_path}/csvfile/all_code.csv'

# 配置的路径
config_path = f'{project_path}/csvfile/config.csv'
trade_date_path = f'{project_path}/csvfile/trade_date.csv'
pool_config_path = f'{project_path}/csvfile/pool_config.csv'

# 行业板块
industry_board_path = f'{project_path}/csvfile/industry_board.csv'

# 测试路径
tmp_path = f'{project_path}tmp.csv'

# 字体路径
text_font = f'{project_path}/font/SourceHanSansSC-Bold.otf'
