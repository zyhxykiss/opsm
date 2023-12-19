import numpy as np
from Config.my_Enum import Label
from Config.my_Enum import PersonalCharacter as PC
from Config.my_Enum import ApproximateNumber as AN
from map.data_map_generation import my_choice
from Config.my_Enum import Place
import pandas as pd
from Config.param_config import param
from abc import ABCMeta
from abc import abstractmethod


def normal_trunc(loc=0.0, scale=0.1, min=0.0, max=0.05):
    p = np.random.normal(loc, scale)
    while (p <= min) or (p > max):
        p = np.random.normal(loc, scale)
    return p


def normal_choice(choice_object: list, lower_limit=-2.0, upper_limit=2.0) -> int:
    """
    给定一个列表，按正态分布从中选出其中一个元素
    :param choice_object: 选择列表
    :param lower_limit: 正态分布下界
    :param upper_limit: 正态分布上界
    :return: 选择出的元素
    """
    judge = np.random.normal()
    while (judge < lower_limit) & (judge > upper_limit):
        judge = np.random.normal()

    interval = (upper_limit - lower_limit) / len(choice_object)
    for i in range(0, len(choice_object)):
        if judge <= lower_limit + interval * (i + 1):
            return choice_object[i]
    return choice_object[-1]


def normal_noise():
    return normal_trunc(loc=0, scale=0.1, min=-param["noise_upper_limit"], max=param["noise_upper_limit"])


class BasePerson(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self, attributes: dict, select_map=None):
        self.id = attributes["id"]
        if select_map is None:
            self.probability_map = self.reload_probability_map(attributes['probability_map'])  # 覆盖概率
        else:
            self.probability_map = self.reload_probability_as_select(attributes['probability_map'], select_map)  # 覆盖概率
        self.charge = attributes['charge']  # 要价
        self.allocated = 0
        self.pi = 0  # 拍卖成功后得到的回报
        self.marginal_value = 0  # 边际价值
        self.marginal_density = 0  # 边际密度

    def reload_probability_as_select(self, pro_map: list, select_map: list):
        reload = []
        for i in range(0, param["map_rows"]):
            for j in range(0, param["map_columns"]):
                if select_map[i][j] == 1:
                    reload.append(pro_map[i][j])
        return reload

    def reload_probability_map(self, probability_map):
        reload = []
        for line in probability_map:
            for elem in line:
                if elem != 0:
                    reload.append(elem)
        return reload

    def to_dict_base(self):
        return {
            "id": self.id,
            "charge": self.charge,
            "pi": self.pi,
            "marginal_value": self.marginal_value,
            "marginal_density": self.marginal_density
        }


class Person(BasePerson):

    def __init__(self, id=0, data_map_file="", attributes=None, select_map=None):
        if attributes is None:
            self.map_rows = param["map_rows"]
            self.map_columns = param["map_columns"]
            self.id = id
            self.dormitory = self.set_dormitory()
            self.canteen = self.set_canteen()
            self.academy = self.set_academy()
            self.character = self.set_character()
            self.like_sport = self.set_like_sports()
            self.like_read = self.set_like_read()
            self.like_long_run = self.set_like_long_run()
            self.easy_ill = self.set_easy_ill()
            self.course_amount = self.set_course_amount()
            self.accustom_place = self.set_accustoms_place()
            self.initiate_point = [0.0, 0.0]
            self.probability_map = self.generate_probability_map(data_map_file)
            self.charge = self.generate_charge()

        else:
            super().__init__(attributes, select_map)

    def set_character(self):
        """
        设置任务性格，按标准正态分布取值
        :return:
        """
        return normal_choice([PC.ESPECIALLY_INACTIVITY.value, PC.INACTIVITY.value, PC.ACTIVITY.value,
                              PC.VERY_ACTIVITY.value, PC.HIGHLY_ACTIVITY.value])

    def set_course_amount(self):
        """
        设置课程多少，按标准正态分布取值
        :return:
        """
        return normal_choice([AN.RARELY.value, AN.LITTLE.value, AN.ORDINARY.value])

    def set_dormitory(self):
        """
        设置所在学生公寓，按宿舍多寡分布
        :return:
        """
        return my_choice([i for i in range(Label.QIU_DORMITORY1.value, Label.FU_DORMITORY.value + 1)],
                         [0.2, 0.1, 0.25, 0.15, 0.2, 0.1])

    def set_academy(self):
        """
        设置学生所属学院，与所在宿舍有关
        :return:
        """
        if Label.QIU_DORMITORY1.value <= self.dormitory <= Label.QIU_DORMITORY2.value:
            choice_amount = Label.INFO_ACADEMY.value - Label.BIO_ACADEMY.value
            return my_choice([i for i in range(Label.BIO_ACADEMY.value, Label.INFO_ACADEMY.value)],
                             [1 / choice_amount for _ in range(0, choice_amount)])

        elif self.dormitory == Label.NAN_DORMITORY.value:
            choice_amount = Label.MOOT_COURT.value - Label.SOURCE_ENVIR_ACADEMY.value
            return my_choice([i for i in range(Label.SOURCE_ENVIR_ACADEMY.value, Label.MOOT_COURT.value)],
                             [1 / choice_amount for _ in range(0, choice_amount)])

        elif Label.HUA_DORMITORY.value <= self.dormitory <= Label.ZI_DORMITORY.value:
            choice_amount = Label.NEWS_ACADEMY.value - Label.LAW_ACADEMY.value
            return my_choice([i for i in range(Label.LAW_ACADEMY.value, Label.NEWS_ACADEMY.value)],
                             [1 / choice_amount for _ in range(0, choice_amount)])

        else:
            return my_choice([Label.ASTRONOMY_ACADEMY.value, Label.ATTACHED_SCHOOL.value], [0.3, 0.7])

    def set_like_sports(self) -> bool:
        """
        设置是否喜爱运动，与任务性格有关
        :return:
        """
        if (self.character == PC.ESPECIALLY_INACTIVITY.value) and (np.random.random() < 0.1):
            return True

        if (self.character == PC.INACTIVITY.value) and (np.random.random() < 0.2):
            return True

        if (self.character == PC.ACTIVITY.value) and (np.random.random() < 0.3):
            return True

        if (self.character == PC.VERY_ACTIVITY.value) and (np.random.random() < 0.4):
            return True

        if (self.character == PC.HIGHLY_ACTIVITY.value) and (np.random.random() < 0.5):
            return True
        return False

    def set_like_read(self) -> bool:
        """
        设置爱是否喜欢读书
        :return:
        """
        if np.random.random() < 0.1:
            return True
        else:
            return False

    def set_like_long_run(self) -> bool:
        """
        设置时候喜欢长跑，只有喜欢运动的人才能喜欢长跑
        :return:
        """
        if self.like_sport and (np.random.random() < 0.08):
            return True
        else:
            return False

    def set_easy_ill(self) -> bool:
        """
        设置是否容易生病, 与是否喜爱运动有关
        :return:
        """
        if self.like_sport and (np.random.random() < 0.005):
            return True
        if (not self.like_sport) and (np.random.random() < 0.01):
            return True
        return False

    def set_canteen(self) -> int:
        """
        选择离得近的食堂
        :return:
        """
        if self.dormitory == Label.ZI_DORMITORY.value:
            return Label.ZI_CANTEEN.value
        elif self.dormitory == Label.HUA_DORMITORY.value:
            if np.random.random() > 0.5:
                return Label.ZI_CANTEEN.value
            else:
                return Label.NAN_CANTEEN.value
        else:
            return Label.NAN_CANTEEN.value

    def set_accustoms_place(self) -> list:
        """
        选择喜欢去的地方
        :return:
        """
        accustoms_place = [self.dormitory, self.canteen]

        if self.like_sport:
            accustoms_place.append(my_choice([i for i in range(
                Label.INSTRUMENT_FIELD.value, Label.TENNIS_FIELD.value + 1)], [0.1, 0.2, 0.15, 0.2, 0.2, 0.15]))

        if self.like_read:
            accustoms_place.append(Label.LIBRARY.value)

        if self.easy_ill:
            accustoms_place.append(Label.HOSPITAL.value)

        if self.character == PC.ESPECIALLY_INACTIVITY.value:
            amount_accustoms_place = np.random.choice([2, 3])
            if amount_accustoms_place > len(accustoms_place):
                accustoms_place = accustoms_place + self.select_place(amount_accustoms_place - len(accustoms_place))

        elif self.character == PC.INACTIVITY.value:
            amount_accustoms_place = np.random.choice([3, 4])
            if amount_accustoms_place > len(accustoms_place):
                accustoms_place = accustoms_place + self.select_place(amount_accustoms_place - len(accustoms_place))

        elif self.character == PC.ACTIVITY.value:
            amount_accustoms_place = np.random.choice([4, 5])
            if amount_accustoms_place > len(accustoms_place):
                accustoms_place = accustoms_place + self.select_place(amount_accustoms_place - len(accustoms_place))

        elif self.character == PC.VERY_ACTIVITY.value:
            amount_accustoms_place = np.random.choice([5, 6])
            if amount_accustoms_place > len(accustoms_place):
                accustoms_place = accustoms_place + self.select_place(amount_accustoms_place - len(accustoms_place))

        elif self.character == PC.HIGHLY_ACTIVITY.value:
            amount_accustoms_place = np.random.choice([6, 10])
            if amount_accustoms_place > len(accustoms_place):
                accustoms_place = accustoms_place + self.select_place(amount_accustoms_place - len(accustoms_place))

        return accustoms_place

    def select_place(self, amount_accustoms_place):
        places = []
        while amount_accustoms_place > len(places):
            place = my_choice(list(Place.keys()), list(Place.values()))
            if place not in places:
                places.append(place)
        return places

    def get_visit_probability(self):
        """
        随机生成每个点的访问概率
        :return:
        """
        if self.character == PC.ESPECIALLY_INACTIVITY.value:
            return normal_trunc(0.02, 0.1, 0.01, 0.1)
        elif self.character == PC.INACTIVITY.value:
            return normal_trunc(loc=0.04, scale=0.1, min=0.01, max=0.12)
        elif self.character == PC.ACTIVITY.value:
            return normal_trunc(loc=0.06, scale=0.1, min=0.01, max=0.14)
        elif self.character == PC.VERY_ACTIVITY.value:
            return normal_trunc(loc=0.08, scale=0.1, min=0.01, max=0.16)
        else:
            return normal_trunc(loc=0.1, scale=0.1, min=0.01, max=0.18)

    def find_all_label(self, data_map, label):
        """
        返回数字地图中同一label的位置信息
        :param data_map:
        :param label: 要找的label
        :return: 返回一个列表，列表的元素为[row, col]形式
        """
        labels = []
        try:
            select_map = data_map.where(data_map == label)
            select_map = select_map.dropna(thresh=1)
            for row in select_map.index:
                for col in select_map.columns:
                    if not pd.isnull(select_map.loc[row, col]):
                        labels.append([row, int(data_map.columns.tolist().index(col))])
            return labels
        except:
            print("label" + str(label))
            exit(0)

    def find_all_labels(self, data_map, labels: list) -> dict:
        """
        返回数字地图中同一label的位置信息
        :param data_map:
        :param label: 要找的label
        :return: 返回一个列表，列表的元素为[row, col]形式
        """
        labels_points = {}
        for label in labels:
            labels_points[label] = self.find_all_label(data_map, label)
        return labels_points

    def born_point(self, data_map: pd.DataFrame) -> list:
        """
        25%出生在宿舍，10%出生在食堂，20%出生在学院楼， 30%出生在教学楼，15%出现在其他地方
        :param data_map:
        :return: 返回一歌DATAFRAME位置，有index和columns组成
        """
        place = my_choice([1, 2, 3, 4, 5], [0.25, 0.1, 0.2, 0.3, 0.15])
        if place == 1:
            dormitorys = self.find_all_label(data_map, self.dormitory)
            return my_choice(dormitorys, [1.0 / len(dormitorys) for _ in range(len(dormitorys))])
        elif place == 2:
            canteens = self.find_all_label(data_map, self.canteen)
            return my_choice(canteens, [1.0 / len(canteens) for _ in range(len(canteens))])
        elif place == 3:
            teaching_builds = self.find_all_label(data_map, self.select_teaching_build())
            return my_choice(teaching_builds, [1.0 / len(teaching_builds) for _ in range(len(teaching_builds))])
        elif place == 4:
            academys = self.find_all_label(data_map, self.academy)
            return my_choice(academys, [1.0 / len(academys) for _ in range(len(academys))])
        else:
            return self.select_point_random(data_map)

    def select_teaching_build(self) -> int:
        """
        按一定概率返回一栋教学楼的label
        :return:
        """
        if Label.QIU_DORMITORY1.value <= self.dormitory <= Label.NAN_DORMITORY.value:
            return my_choice([i for i in range(Label.GEWU_BUILD.value, Label.ZHONGSHAN_BUILD.value + 1)],
                             [0.5, 0.3, 0.15, 0.05])

        elif self.dormitory == Label.HUA_DORMITORY.value:
            return my_choice([i for i in range(Label.GEWU_BUILD.value, Label.ZHONGSHAN_BUILD.value + 1)],
                             [0.2, 0.3, 0.3, 0.2])

        elif self.dormitory == Label.ZI_DORMITORY.value:
            return my_choice([i for i in range(Label.GEWU_BUILD.value, Label.ZHONGSHAN_BUILD.value + 1)],
                             [0.2, 0.05, 0.6, 0.15])

        elif self.academy != Label.ATTACHED_SCHOOL.value and self.dormitory == Label.FU_DORMITORY.value:
            return my_choice([i for i in range(Label.GEWU_BUILD.value, Label.ZHONGSHAN_BUILD.value + 1)],
                             [0.3, 0.5, 0.15, 0.05])
        if self.academy == Label.ATTACHED_SCHOOL.value:
            return Label.ATTACHED_SCHOOL.value

    def select_point_random(self, data_map: pd.DataFrame) -> list:
        """
        随机返回data_map中的一个点，这个点不能在荒地上
        :param data_map:
        :return:
        """
        i = np.random.choice(range(self.map_rows))
        j = np.random.choice(range(self.map_columns))
        while data_map.iloc[i, j] == 0:
            i = np.random.choice(range(self.map_rows))
            j = np.random.choice(range(self.map_columns))
        return [i, j]

    def set_probability(self, gp_map, point, point_probability, loss_interval):
        """
        给定一个点和该点的概率，并按一定衰减率向四周衰减
        :param data_map: 数字地图
        :param gp_map: 个人概率地图
        :param point: 给定点
        :param point_probability: 给定点的改率
        :param loss_interval: 衰减间隔
        :return: none
        """
        if ((point[0] > self.map_rows) or (point[0] < 0)) or ((point[1] > self.map_columns) or (point[1] < 0)):
            return

        upper_pro = point_probability - loss_interval + normal_noise()
        ul_pro = point_probability - loss_interval + normal_noise()
        left_pro = point_probability - loss_interval + normal_noise()
        dl_pro = point_probability - loss_interval + normal_noise()
        down_pro = point_probability - loss_interval + normal_noise()
        dr_pro = point_probability - loss_interval + normal_noise()
        right_pro = point_probability - loss_interval + normal_noise()
        ur_pro = point_probability - loss_interval + normal_noise()
        # u
        if point[0] + 1 < self.map_rows:
            if (upper_pro > gp_map[point[0] + 1, point[1]]) and (gp_map[point[0] + 1, point[1]] != 0):
                gp_map[point[0] + 1, point[1]] = upper_pro
                self.set_probability(gp_map, [point[0] + 1, point[1]], upper_pro, loss_interval)
        # ul
        if (point[0] + 1 < self.map_rows) and (point[1] - 1 > 0):
            if (ul_pro > gp_map[point[0] + 1, point[1] - 1]) and (gp_map[point[0] + 1, point[1] - 1] != 0):
                gp_map[point[0] + 1, point[1] - 1] = ul_pro
                self.set_probability(gp_map, [point[0] + 1, point[1] - 1], ul_pro, loss_interval)
        # l
        if point[1] - 1 > 0:
            if (left_pro > gp_map[point[0], point[1] - 1]) and (gp_map[point[0], point[1] - 1] != 0):
                gp_map[point[0], point[1] - 1] = left_pro
                self.set_probability(gp_map, [point[0], point[1] - 1], left_pro, loss_interval)
        # ur
        if (point[0] + 1 < self.map_rows) and (point[1] + 1 < self.map_columns):
            if (ur_pro > gp_map[point[0] + 1, point[1] + 1]) and (gp_map[point[0] + 1, point[1] + 1] != 0):
                gp_map[point[0] + 1, point[1] + 1] = ur_pro
                self.set_probability(gp_map, [point[0] + 1, point[1] + 1], ur_pro, loss_interval)
        # d
        if point[0] - 1 > 0:
            if (down_pro > gp_map[point[0] - 1, point[1]]) and (gp_map[point[0] - 1, point[1]] != 0):
                gp_map[point[0] - 1, point[1]] = down_pro
                self.set_probability(gp_map, [point[0] - 1, point[1]], down_pro, loss_interval)
        # dr
        if (point[0] - 1 > 0) and (point[1] + 1 < self.map_columns):
            if (dr_pro > gp_map[point[0] - 1, point[1] + 1]) and (gp_map[point[0] - 1, point[1] + 1] != 0):
                gp_map[point[0] - 1, point[1] + 1] = dr_pro
                self.set_probability(gp_map, [point[0] - 1, point[1] + 1], dr_pro, loss_interval)
        # r
        if point[1] + 1 < self.map_columns:
            if (right_pro > gp_map[point[0], point[1] + 1]) and (gp_map[point[0], point[1] + 1] != 0):
                gp_map[point[0], point[1] + 1] = right_pro
                self.set_probability(gp_map, [point[0], point[1] + 1], right_pro, loss_interval)
        # dl
        if (point[0] - 1 > 0) and (point[1] - 1 > 0):
            if (dl_pro > gp_map[point[0] - 1, point[1] - 1]) and (gp_map[point[0] - 1, point[1] - 1] != 0):
                gp_map[point[0] - 1, point[1] - 1] = dl_pro
                self.set_probability(gp_map, [point[0] - 1, point[1] - 1], dl_pro, loss_interval)

        return

    def set_point_probability(self, gp_map, point, pro):
        if pro > gp_map[point[0], point[1]]:
            gp_map[point[0], point[1]] = pro

    def generate_probability_map(self, data_map_file="") -> np.array:
        """
        生成个人概率矩阵
        :param data_map:
        :return:
        """
        interval_param = list(param["loss_interval"][self.character].values())
        pro_param = list(param["initiate_probability"][self.character].values())
        academy_param = list(param["academy_probability"].values())
        tb_param = list(param["tb_probability"].values())

        gp_map = np.array(np.zeros(self.map_rows * self.map_columns), dtype=float). \
            reshape(self.map_rows, self.map_columns)
        if data_map_file == "":
            return np.zeros(self.map_rows * self.map_columns).tolist()

        data_map = pd.read_csv(data_map_file)

        for i in range(self.map_rows):
            for j in range(self.map_columns):
                if data_map.iloc[i, j] != 0:
                    gp_map[i, j] = self.get_visit_probability()

        # TT = 0
        # for i in range(self.map_rows):
        #     for j in range(self.map_columns):
        #         if gp_map[i, j] < 641:
        #             TT += 1

        # 设置出生点
        born_point = self.born_point(data_map)
        self.initiate_point = born_point
        self.set_point_probability(gp_map, born_point, 1)
        self.set_probability(gp_map, born_point, 1,
                             normal_trunc(interval_param[0], interval_param[1], interval_param[2], interval_param[3]))

        # 喜欢长跑
        if self.like_long_run:
            road = self.find_all_labels(data_map,
                                        [i for i in range(Label.GUANGTIAN_NORTH.value, Label.GUANGTIAN_WEST.value + 1)])
            for value in road.values():
                for point in value:
                    self.set_point_probability(gp_map, point, normal_trunc(0.3, 0.1, 0.2, 0.4))

        # 经常去的地方
        for place in self.accustom_place:
            if (place == Label.ZE_LAKE.value) or (place == Label.BELL_TOWER.value):
                continue
            all_places = self.find_all_label(data_map, place)
            select_place = my_choice(all_places, [1.0 / len(all_places) for _ in range(len(all_places))])

            if select_place:
                self.set_point_probability(gp_map, select_place,
                                           normal_trunc(pro_param[0], pro_param[1], pro_param[2], pro_param[3]))

                self.set_probability(gp_map, select_place, gp_map[select_place[0], select_place[1]],
                                     normal_trunc(interval_param[0], interval_param[1], interval_param[2],
                                                  interval_param[3]))

        # 学院
        academys = self.find_all_label(data_map, self.academy)
        academy = my_choice(academys, [1.0 / len(academys) for _ in range(len(academys))])
        self.set_point_probability(gp_map, academy,
                                   normal_trunc(academy_param[0], academy_param[1], academy_param[2], academy_param[3]))

        self.set_probability(gp_map, academy, gp_map[academy[0], academy[1]],
                             normal_trunc(interval_param[0], interval_param[1],
                                          interval_param[2], interval_param[3]))

        # 教学楼
        teaching_builds = []
        while len(teaching_builds) < self.course_amount:
            teaching_build = self.select_teaching_build()
            if teaching_build not in teaching_builds:
                teaching_builds.append(teaching_build)
            if teaching_build == Label.ATTACHED_SCHOOL.value:
                break
        for tb in teaching_builds:
            map_tds = self.find_all_label(data_map, tb)
            map_tb = my_choice(map_tds, [1.0 / len(map_tds) for _ in range(len(map_tds))])
            self.set_point_probability(gp_map, map_tb, normal_trunc(tb_param[0], tb_param[1], tb_param[2], tb_param[3]))
            self.set_probability(gp_map, map_tb, gp_map[map_tb[0], map_tb[1]],
                                 normal_trunc(interval_param[0], interval_param[1],
                                              interval_param[2], interval_param[3]))

        TT = 0
        for i in range(self.map_rows):
            for j in range(self.map_columns):
                if gp_map[i, j] > 0:
                    TT += 1

        gp_map = np.around(gp_map, decimals=2)

        return gp_map

    def generate_charge(self):
        bid_base = param["bid_base"]
        return bid_base[self.character] * np.random.uniform(0.5, 2)

    def to_dict(self):
        return {
            "id": self.id,
            "dormitory": self.dormitory,
            "canteen": self.canteen,
            "academy": self.academy,
            "character": self.character,
            "like_sport": self.like_sport,
            "like_read": self.like_read,
            "like_long_run": self.like_long_run,
            "easy_ill": self.easy_ill,
            "course_amount": self.course_amount,
            "accustom_place": self.accustom_place,
            "initiate_point": self.initiate_point,
            "charge": self.charge,
            "probability_map": self.probability_map
        }

    def to_dict_base(self):
        return BasePerson.to_dict_base(self)

