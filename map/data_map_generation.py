import numpy as np
from Config.my_Enum import Label
from Config.my_Enum import PointWeight as PW
import pandas as pd
import random
from Config.param_config import param


def my_choice(action_list: list, p: list):
    """
    :param action_list: 被选择的列表
    :param p: 概率列表
    :return: 被选中的值
    """
    judge = random.random()
    for i in range(len(p)):
        if judge <= sum(p[0:i+1]):
            return action_list[i]


class DataMap:

    def __init__(self):
        self.map_rows = param["map_rows"]
        self.map_columns = param["map_columns"]

    def data_map_maker(self):
        data_map = np.array(np.zeros(self.map_rows*self.map_columns), dtype=int).\
            reshape(self.map_rows, self.map_columns)

        '''
            二级小道
        '''
        # 东部校医院片区
        data_map[2:-5, 3] = Label.FOOTPATH.value  # 云大附中至工地
        data_map[3:6, 5] = Label.FOOTPATH.value  # 校医院旁学生公寓南北向
        data_map[3, 5:8] = Label.FOOTPATH.value  # 校医院旁学生公寓东西向

        # 南部生活区、教学区、学院楼
        data_map[1:6, 10] = Label.FOOTPATH.value  # 生科院旁学生公寓南北向
        data_map[1:4, 13] = Label.FOOTPATH.value  # 楸苑二栋左侧
        data_map[1:8, 15] = Label.FOOTPATH.value  # 楸苑庆来南路至物科院
        data_map[3, 13:-6] = Label.FOOTPATH.value  # 楸苑至足球场东西向
        data_map[7:10, 9] = Label.FOOTPATH.value  # 生科院至苍雨南路
        data_map[5: 10, 11] = Label.FOOTPATH.value  # 化工院与软院间南北向
        data_map[5:8, 13] = Label.FOOTPATH.value  # 力行楼与物科院间南北向
        data_map[5:8, 18] = Label.FOOTPATH.value  # 停车场与格物楼二栋之间南北向
        data_map[3:10, 20] = Label.FOOTPATH.value  # 楠苑食堂至苍雨南路
        data_map[1:8, 22] = Label.FOOTPATH.value  # 广田南路至信息学院
        data_map[1:8, 24] = Label.FOOTPATH.value  # 广田南路至经济学院左侧
        data_map[1:10, 26] = Label.FOOTPATH.value  # 广田南路至苍雨南路经经济学院左侧
        data_map[7, 7:31] = Label.FOOTPATH.value  # 生科院至图书馆东辅楼

        # 体育场区
        data_map[1:4, -7] = Label.FOOTPATH.value  # 足球场与篮球场间南北向
        data_map[2, -7:-4] = Label.FOOTPATH.value  # 篮球馆与篮球场间
        data_map[4, -5:-2] = Label.FOOTPATH.value  # 网球场北侧
        data_map[2:9, -5] = Label.FOOTPATH.value  # 篮球场至桦苑

        # 西部生活区、教学区、学院楼
        # 庆来西路以东
        data_map[5:15, -11] = Label.FOOTPATH.value  # 庆来南路经图书馆至学生会堂
        data_map[8, -11:-2] = Label.FOOTPATH.value  # 图书馆前经喷泉至广田西路
        data_map[10, -14:-2] = Label.FOOTPATH.value  # 苍雨西路经图书馆北侧至广田西路
        data_map[11, -11:-6] = Label.FOOTPATH.value  # 模拟法庭北侧至庆来西路
        data_map[11:19, -9] = Label.FOOTPATH.value  # 中山楼与法学院间至文汇楼二栋
        data_map[14, -14:-8] = Label.FOOTPATH.value  # 学生会堂南侧至中山楼
        data_map[18, -13:-8] = Label.FOOTPATH.value  # 学生会堂北侧至文汇楼二栋
        data_map[14:19, -13] = Label.FOOTPATH.value  # 学生会堂后侧小路
        data_map[15, -9:-7] = Label.FOOTPATH.value  # 校庆馆南侧
        data_map[17, -9:-7] = Label.FOOTPATH.value  # 校庆馆北侧
        data_map[18:23, -12] = Label.FOOTPATH.value  # 学生会堂北侧至苍雨西路支路
        data_map[18:23, -10] = Label.FOOTPATH.value  # 文汇楼间南北向
        data_map[20, -12:-2] = Label.FOOTPATH.value  # 文汇楼间至广田西路
        data_map[22, -11:-2] = Label.FOOTPATH.value  # 文汇楼北侧至广田西路
        # 庆来西路以西
        data_map[9:23, -5] = Label.FOOTPATH.value  # 桦苑间至梓源间
        data_map[14, -6:-2] = Label.FOOTPATH.value  # 体育学院与艺术学院之间
        data_map[18, -7:-2] = Label.FOOTPATH.value  # 新闻学院专家公寓与梓苑之间

        # 云山附近
        data_map[11, 9:25] = Label.FOOTPATH.value  # 云山南侧小路
        data_map[10, 8:10] = Label.FOOTPATH.value  # 天文学院南侧
        data_map[10:23, 9] = Label.FOOTPATH.value  # 云山东侧天文学院后
        data_map[11:22, 24] = Label.FOOTPATH.value  # 云山西侧小路
        data_map[22, 7:27] = Label.FOOTPATH.value  # 云山北侧，明远楼前
        data_map[20:23, -23] = Label.FOOTPATH.value  # 明远楼东侧
        data_map[20:23, -19] = Label.FOOTPATH.value  # 明远楼西侧
        data_map[20, -23:-19] = Label.FOOTPATH.value  # 明远楼南侧东西向
        data_map[19, -22:-15] = Label.FOOTPATH.value  # 明远楼北侧至钟楼
        data_map[18:21, -16] = Label.FOOTPATH.value  # 钟楼西侧
        data_map[20, -17:-14] = Label.FOOTPATH.value  # 钟楼南侧薰衣草田
        data_map[20:22, -15] = Label.FOOTPATH.value  # 薰衣草田南北向

        '''
            一级主干道
        '''
        #  广田路
        data_map[1, 7:-1] = Label.GUANGTIAN_SOUTH.value  # 广田南路
        data_map[0:-1, 7] = Label.GUANGTIAN_EAST.value  # 广田东路
        data_map[1:-1, -2] = Label.GUANGTIAN_WEST.value  # 广田西路
        data_map[-2, 7:-1] = Label.GUANGTIAN_NORTH.value  # 广田北路
        data_map[4, -1] = Label.GUANGTIAN_WEST.value  # 西二门

        # 庆来路
        data_map[5, 0:-6] = Label.QINGLAI_SOUTH.value  # 庆来南路
        data_map[5:-1, -7] = Label.QINGLAI_WEST.value  # 庆来西路

        # 雨苍路
        data_map[9, 7:-13] = Label.CANGYU_SOUTH.value  # 雨苍南路
        data_map[9:-6, -14] = Label.CANGYU_WEST.value  # 雨苍西路
        data_map[-9, -14:-11] = Label.CANGYU_WEST.value  # 雨苍西路支路
        data_map[-9:-1, -12] = Label.CANGYU_WEST.value  # 雨苍西路支路
        data_map[-7, 7:-13] = Label.CANGYU_WEST.value  # 雨苍北路

        # 百家大道
        data_map[16, -7:] = Label.GUANGTIAN_WEST.value

        # 致公大道
        data_map[-9:, -21] = Label.GUANGTIAN_NORTH.value

        # 南门至苍雨南路
        data_map[0: 6, 17] = Label.CANGYU_SOUTH.value  # 南门至庆来南路
        data_map[5:10, 16] = Label.QINGLAI_SOUTH.value  # 庆来南路至苍雨南路

        '''
            学生公寓
        '''
        # 附中旁学生公寓
        data_map[3:5, 4] = Label.FU_DORMITORY.value  # 附中旁东侧学生公寓
        data_map[4, 6] = Label.FU_DORMITORY.value  # 附中旁西侧学生公寓

        # 楸苑二期学生公寓
        data_map[2:5, 9] = Label.QIU_DORMITORY2.value  # 楸苑二期东侧学生公寓
        data_map[2:5, 11] = Label.QIU_DORMITORY2.value  # 楸苑二期西侧学生公寓

        # 楸苑一期学生公寓
        data_map[2, 14] = Label.QIU_DORMITORY1.value  # 楸苑一期楸苑二栋
        data_map[2, 16] = Label.QIU_DORMITORY1.value  # 楸苑一期楸苑一栋
        data_map[4, 14] = Label.QIU_DORMITORY1.value  # 楸苑一期楸苑四栋
        data_map[4, 16] = Label.QIU_DORMITORY1.value  # 楸苑一期楸苑三栋

        # 楠苑学生公寓
        data_map[4, 21] = Label.NAN_DORMITORY.value  # 楠苑五栋
        data_map[2, 23] = Label.NAN_DORMITORY.value  # 楠苑三栋
        data_map[4, 23] = Label.NAN_DORMITORY.value  # 楠苑四栋
        data_map[2, 25] = Label.NAN_DORMITORY.value  # 楠苑一栋
        data_map[4, 25] = Label.NAN_DORMITORY.value  # 楠苑二栋

        # 桦苑学生公寓
        data_map[9, -6] = Label.HUA_DORMITORY.value  # 桦苑1栋
        data_map[9, -4:-2] = Label.HUA_DORMITORY.value  # 桦苑三栋
        data_map[11, -6] = Label.HUA_DORMITORY.value  # 桦苑二栋

        # 梓源学生公寓
        data_map[19, -6] = Label.ZI_DORMITORY.value  # 梓苑三栋
        data_map[19, -4] = Label.ZI_DORMITORY.value  # 梓苑一栋
        data_map[21, -6] = Label.ZI_DORMITORY.value  # 梓苑四栋
        data_map[21, -4] = Label.ZI_DORMITORY.value  # 梓苑二栋

        '''
            教学楼
        '''
        # 力行楼
        data_map[6, 12] = Label.LIXING_BUILD.value  # 力行楼

        # 格物楼
        data_map[6, 19] = Label.GEWU_BUILD.value  # 格物楼二栋
        data_map[6, 21] = Label.GEWU_BUILD.value  # 格物楼一栋

        # 文汇楼
        data_map[19, -11] = Label.WENHUI_BUILD.value  # 文汇楼一栋
        data_map[19, -9] = Label.WENHUI_BUILD.value  # 文汇楼二栋
        data_map[21, -11] = Label.WENHUI_BUILD.value  # 文汇楼四栋
        data_map[21, -9] = Label.WENHUI_BUILD.value  # 文汇楼三栋

        # 中山楼
        data_map[12:14, -7] = Label.ZHONGSHAN_BUILD.value  # 中山楼

        '''
            学院楼
        '''
        data_map[6, 8:10] = Label.BIO_ACADEMY.value  # 生科院
        data_map[11:13, 8] = Label.ASTRONOMY_ACADEMY.value  # 天文学院
        data_map[8, 10] = Label.CHEMISTRY_ACADEMY.value  # 化工学院
        data_map[8, 12] = Label.SOFTWARE_ACADEMY.value  # 软件学院
        data_map[6, 14] = Label.PHYSICAL_ACADEMY.value  # 物科院
        data_map[8, 17:19] = Label.SOURCE_ENVIR_ACADEMY.value  # 资环学院
        data_map[8, 19] = Label.ARCHITECTURE_ACADEMY.value  # 城建学院
        data_map[8, 21:23] = Label.INFO_ACADEMY.value  # 信息学院
        data_map[6, 25] = Label.ECONOMIC_ACADEMY.value  # 经济学院
        data_map[12, -9] = Label.MOOT_COURT.value  # 模拟法庭
        data_map[13, -9] = Label.LAW_ACADEMY.value  # 法学院
        data_map[13, -4] = Label.SPORT_ACADEMY.value  # 体育学院
        data_map[15, -4] = Label.ART_ACADEMY.value  # 艺术学院
        data_map[15, -6] = Label.BUSINESS_ACADEMY.value  # 商学院
        data_map[17, -6] = Label.NEWS_ACADEMY.value  # 新闻学院

        '''
            辅助建筑
        '''
        data_map[1:3, 1:5] = Label.ATTACHED_SCHOOL.value  # 附属中学
        data_map[6:8, 5:7] = Label.HOSPITAL.value  # 校医院
        data_map[10:15, 5:7] = Label.BIO_EXPERIMENT_BASE.value  # 生物实验基地
        data_map[8, 8] = Label.EXPER_WASTE_CENTER.value  # 实验废物处理中心
        data_map[6, 17] = Label.BUS_BASE.value  # 汽车站
        data_map[2, 20:22] = Label.NAN_CANTEEN.value  # 楠苑食堂
        data_map[4, 18:20] = Label.NAN_MIX_BUILD.value  # 楠苑综合楼
        data_map[6, -11] = Label.EAST_AUXILIARY_BUILD.value  # 图书馆东辅楼
        data_map[8:10, -13:-11] = Label.LIBRARY.value  # 图书馆
        data_map[9, -8] = Label.WEST_AUXILIARY_BUILD.value  # 图书馆西辅楼
        data_map[15:18, -12:-10] = Label.STUDENT_HALL.value  # 学生会堂
        data_map[-8:-6, -6:-4] = Label.ZI_CANTEEN.value  # 梓苑食堂
        data_map[17, -4] = Label.EXPERT_DORMITORY.value  # 专家公寓
        data_map[21, -22:-19] = Label.MINGYUAN_BUILD.value  # 明远楼
        data_map[28, -22] = Label.PALEON_INSTITUTE.value  # 古生物研究所
        data_map[28, -20] = Label.INFO_TECH_CENTER.value  # 信息技术中心
        data_map[6:8, -10:-7] = Label.SQUARE.value  # 图书馆广场
        data_map[7, -9] = Label.WASTELAND.value  # 将喷泉位置设置为荒地
        data_map[15:18, -10] = Label.SQUARE.value  # 文典广场

        '''
            运动场
        '''
        data_map[2, -12] = Label.INSTRUMENT_FIELD.value  # 器械厂
        data_map[2, -11] = Label.BADMINTON_GYM.value  # 羽毛球馆
        data_map[2, -10:-7] = Label.FOOTBALL_FIELD.value  # 足球场
        data_map[2:4, -4] = Label.BASKETBALL_FIELD.value  # 篮球场
        data_map[3:5, -6] = Label.BASKETBALL_GYM.value  # 篮球馆
        data_map[2:4, -3] = Label.TENNIS_FIELD.value  # 网球场
        data_map[11:13, -4:-2] = Label.FOOTBALL_FIELD.value  # 小足球场

        return data_map

    def weight_distribute_maker(self, data_map: np.array) -> np.array:
        """
        设置每个点的重要性
        :param data_map:数字地图
        :return: 权值矩阵
        """
        weight_map = np.array(np.zeros(self.map_rows * self.map_columns), dtype=int). \
            reshape(self.map_rows, self.map_columns)

        for i in range(self.map_rows):
            for j in range(self.map_columns):
                if ((5 <= i <= 25) and (j == 3)) or ((i == 11) and (10 <= j <= 24)) or ((11 <= i <= 17) and j == 24):
                    weight_map[i, j] = my_choice([PW.UNIMPORTANT.value, PW.PRIMARY_IMPORTANT.value], [0.7, 0.3])
                    continue
                weight_map[i][j] = self.elem_divert(data_map[i, j])
        return weight_map

    def elem_divert(self, elem: int) -> int:
        """
        按一定规则生成该点的权重
        :param elem: 点的LABEL
        :return: 点的权重
        """
        # 荒地
        if elem == Label.WASTELAND.value:
            return PW.ESPECIALLY_UNIMPORTANT.value

        # 道路
        # 广田路
        elif Label.GUANGTIAN_SOUTH.value <= elem <= Label.GUANGTIAN_WEST.value:
            return my_choice([PW.UNIMPORTANT.value, PW.PRIMARY_IMPORTANT.value], [0.7, 0.3])
        # 苍雨路
        elif Label.CANGYU_SOUTH.value <= elem <= Label.CANGYU_NORTH.value:
            return my_choice([PW.UNIMPORTANT.value, PW.PRIMARY_IMPORTANT.value, PW.SECONDARY_IMPORTANT.value],
                             [0.5, 0.3, 0.2])
        # 其它道路
        elif (Label.QINGLAI_SOUTH.value <= elem <= Label.QINGLAI_WEST.value) or (elem == Label.FOOTPATH.value):
            return my_choice([PW.UNIMPORTANT.value, PW.PRIMARY_IMPORTANT.value, PW.SECONDARY_IMPORTANT.value,
                              PW.THIRD_IMPORTANT.value], [0.1, 0.1, 0.2, 0.6])

        # 学院楼和运动场
        elif (Label.BIO_ACADEMY.value <= elem <= Label.ASTRONOMY_ACADEMY.value) or (
                Label.INSTRUMENT_FIELD.value <= elem <= Label.TENNIS_FIELD.value):
            return my_choice([PW.SIXTH_IMPORTANT.value, PW.SEVENTH_IMPORTANT.value, PW.EIGHT_IMPORTANT.value],
                             [0.3, 0.4, 0.3])

        # 学生公寓
        elif Label.QIU_DORMITORY1.value <= elem <= Label.FU_DORMITORY.value:
            return my_choice([PW.SEVENTH_IMPORTANT.value, PW.EIGHT_IMPORTANT.value, PW.NINTH_IMPORTANT.value],
                             [0.6, 0.3, 0.1])

        # 教学楼
        elif Label.GEWU_BUILD.value <= elem <= Label.ZHONGSHAN_BUILD.value:
            return my_choice([PW.EIGHT_IMPORTANT.value, PW.SEVENTH_IMPORTANT.value], [0.7, 0.3])

        # 校医院
        elif elem == Label.HOSPITAL.value:
            return my_choice([PW.THIRD_IMPORTANT.value, PW.FORTH_IMPORTANT.value], [0.5, 0.5])

        # 附属中学
        elif elem == Label.ATTACHED_SCHOOL.value:
            return my_choice([PW.SECONDARY_IMPORTANT.value, PW.THIRD_IMPORTANT.value], [0.5, 0.5])

        # 汽车站
        elif elem == Label.BUS_BASE.value:
            return my_choice([PW.PRIMARY_IMPORTANT.value, PW.SECONDARY_IMPORTANT.value], [0.5, 0.5])

        # 专家公寓
        elif elem == Label.EXPERT_DORMITORY.value:
            return my_choice([PW.SECONDARY_IMPORTANT.value, PW.THIRD_IMPORTANT.value], [0.5, 0.5])

        # 广场
        elif elem == Label.SQUARE.value:
            return my_choice([PW.FORTH_IMPORTANT.value, PW.FIFTH_IMPORTANT.value], [0.5, 0.5])

        # 信息技术中心和古生物研究所
        elif (elem == Label.INFO_TECH_CENTER.value) or (elem == Label.PALEON_INSTITUTE.value):
            return my_choice([PW.PRIMARY_IMPORTANT.value, PW.SECONDARY_IMPORTANT.value], [0.5, 0.5])

        # 明远楼
        elif elem == Label.MINGYUAN_BUILD.value:
            return my_choice([PW.FIFTH_IMPORTANT.value, PW.SIXTH_IMPORTANT.value], [0.5, 0.5])

        # 校庆馆
        elif elem == Label.CENTENNIAL_HALL.value:
            return my_choice([PW.FORTH_IMPORTANT.value, PW.FIFTH_IMPORTANT.value], [0.5, 0.5])

        # 生物实验基地
        elif elem == Label.BIO_EXPERIMENT_BASE.value:
            return my_choice([PW.THIRD_IMPORTANT.value, PW.FORTH_IMPORTANT.value], [0.5, 0.5])

        # 实验废物处理中心
        elif elem == Label.EXPER_WASTE_CENTER.value:
            return my_choice([PW.PRIMARY_IMPORTANT.value, PW.SECONDARY_IMPORTANT.value], [0.5, 0.5])

        # 图书馆东辅楼西辅楼
        elif (elem == Label.LIBRARY.value) or (elem == Label.EAST_AUXILIARY_BUILD.value) or \
                (elem == Label.WEST_AUXILIARY_BUILD.value):
            return my_choice([PW.FIFTH_IMPORTANT.value, PW.SIXTH_IMPORTANT.value], [0.5, 0.5])

        # 楠苑综合楼
        elif elem == Label.NAN_MIX_BUILD.value:
            return my_choice([PW.SEVENTH_IMPORTANT.value, PW.EIGHT_IMPORTANT.value], [0.4, 0.6])

        # 食堂
        elif (elem == Label.NAN_CANTEEN.value) or (elem == Label.ZI_CANTEEN.value):
            return my_choice([PW.EIGHT_IMPORTANT.value, PW.NINTH_IMPORTANT.value], [0.4, 0.6])

        #  学生会堂
        elif elem == Label.STUDENT_HALL.value:
            return my_choice([PW.FORTH_IMPORTANT.value, PW.FIFTH_IMPORTANT.value], [0.5, 0.5])


if __name__ == "__main__":
    DM = DataMap()
    data_map = DM.data_map_maker()
    columns = [f"X_{i}" for i in range(0, 41)]
    indexs = [f"Y_{i}" for i in range(0, 31)]
    df_data_map = pd.DataFrame(data_map, columns=columns, index=indexs)
    df_data_map.to_csv("../document/data_map.csv", index=False)

    weight_map = DM.weight_distribute_maker(data_map)
    df_weight_map = pd.DataFrame(weight_map, columns=columns, index=indexs)
    df_weight_map.to_csv("../document/weight_map.csv", index=False)
