
from Settings.entity import PLAYER_DIMENSIONS
from block import Block

from Blocks.question_block import QuestionBlock
from Blocks.ground_block import GroundBlock1
from Blocks.brick_block import BrickBlock

INITIAL_POS = 3.5, PLAYER_DIMENSIONS[1]

blocks: list[Block]

blocks = [GroundBlock1(i, j) for i in range(69) for j in range(-1, 1)]

blocks.append(QuestionBlock(16, 5))

blocks.append(BrickBlock(20, 5))
blocks.append(QuestionBlock(21, 5))
blocks.append(BrickBlock(22, 5))
blocks.append(QuestionBlock(23, 5))
blocks.append(BrickBlock(24, 5))

blocks.append(QuestionBlock(22, 9))

blocks.append(BrickBlock(0, 1))

blocks.append(BrickBlock(5, 1))
blocks.append(BrickBlock(5, 2))
blocks.append(BrickBlock(5, 3))
blocks.append(BrickBlock(5, 4))
blocks.append(BrickBlock(5, 5))
blocks.append(BrickBlock(5, 6))
blocks.append(BrickBlock(5, 7))
