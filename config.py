from environs import Env

env = Env()
env.read_env()

MIRO_ACCESS_TOKEN= env.str('MIRO_ACCESS_TOKEN')
BOARD_ID = env.str('BOARD_ID')