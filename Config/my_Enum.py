from enum import Enum


class PassFrequency(Enum):
    """
    该枚举用来描述一个人到达一个地方的频率，与生成个人概率矩阵密切相关
    """
    NOT_OFTEN = 1  # 很不经常
    SELDOM = 2  # 不经常
    OFTEN = 3  # 经常
    USUALLY = 4  # 常常
    VERY_OFTEN = 5  # 很经常


class PersonalCharacter(Enum):
    """
    该枚举用来描述人物性格，性格与个人概率矩阵密切相关
    """
    ESPECIALLY_INACTIVITY = 1  # 极其不活跃
    INACTIVITY = 2  # 不活跃
    ACTIVITY = 3  # 活跃
    VERY_ACTIVITY = 4  # 很活跃
    HIGHLY_ACTIVITY = 5  # 极其活跃


class PointWeight(Enum):
    """
    该枚举用来区分采样点的重要性，人流密度越大越重要，方便评估不同点的需要访问的次数以生成任务矩阵
    """
    ESPECIALLY_UNIMPORTANT = 0  # 不重要-》荒地
    UNIMPORTANT = 1  # 重要-》人流量少的道路-》重要性等级1-2
    PRIMARY_IMPORTANT = 2  # 一级重要 -》人流量不太多的道路和较少人-》重要性等级2-3
    SECONDARY_IMPORTANT = 3  # 二级重要 -》 人流量一般的道路和一般性建筑 -》重要性等级3-6
    THIRD_IMPORTANT = 4  # 三级重要 -》 一般性建筑及人流量大的道路
    FORTH_IMPORTANT = 5  # 四级重要 -》 一般性建筑及人流量大的道路
    FIFTH_IMPORTANT = 6  # 五级重要 -》 一般性建筑及人流量大的道路
    SIXTH_IMPORTANT = 7  # 六级重要 -》 运动场、一般性建筑、和学院楼 -》重要性等级7-8
    SEVENTH_IMPORTANT = 8  # 七级重要 -》 运动场、学院楼、学生公寓
    EIGHT_IMPORTANT = 9  # 八级重要 -》 运动场、学院楼、学生公寓及食堂
    NINTH_IMPORTANT = 10  # 九级重要 -》 教学楼、食堂及学生公寓


class Label(Enum):  # 数字地图中的标识
    """
    该枚举用来标记数字地图中不同的不同建筑类型
    """
    # 环境
    WASTELAND = 0  # 荒地
    GUANGTIAN_SOUTH = 1  # 广田南路
    GUANGTIAN_NORTH = 2  # 广田北路
    GUANGTIAN_EAST = 3  # 广田东路
    GUANGTIAN_WEST = 4  # 广田西路
    QINGLAI_SOUTH = 5  # 庆来南路
    QINGLAI_WEST = 6  # 庆来西路
    CANGYU_SOUTH = 7  # 苍雨南路
    CANGYU_WEST = 8  # 苍雨西路
    CANGYU_NORTH = 9  # 苍雨北路
    FOOTPATH = 10  # 二级小路

    # 学生公寓
    QIU_DORMITORY1 = 11  # 学生公寓-楸苑1期
    QIU_DORMITORY2 = 12  # 学生公寓-楸苑2期
    NAN_DORMITORY = 13  # 学生公寓-楠苑
    HUA_DORMITORY = 14  # 学生公寓-桦苑
    ZI_DORMITORY = 15  # 学生公寓-梓苑
    FU_DORMITORY = 16  # 云大附中学生公寓

    # 教学楼
    GEWU_BUILD = 17  # 格物楼
    LIXING_BUILD = 18  # 力行楼
    WENHUI_BUILD = 19  # 文汇楼
    ZHONGSHAN_BUILD = 20  # 中山楼

    # 附加建筑
    HOSPITAL = 21  # 校医院
    ATTACHED_SCHOOL = 22  # 附属中学
    BUS_BASE = 23  # 停车场
    EXPERT_DORMITORY = 24  # 专家公寓
    SQUARE = 25  # 广场
    DRIVER_SCHOOL = 26  # 云大驾校
    BELL_TOWER = 27  # 钟楼
    ZE_LAKE = 28  # 泽湖
    INFO_TECH_CENTER = 29  # 信息技术中心
    PALEON_INSTITUTE = 30  # 古生物研究所
    MINGYUAN_BUILD = 31  # 明远楼
    CENTENNIAL_HALL = 32  # 校庆馆
    BIO_EXPERIMENT_BASE = 33  # 生物实验基地
    EXPER_WASTE_CENTER = 34  # 实验废物处理中心
    LIBRARY = 35  # 图书馆
    WEST_AUXILIARY_BUILD = 36  # 西辅楼
    EAST_AUXILIARY_BUILD = 37  # 东辅楼
    ZI_CANTEEN = 38  # 梓苑食堂
    NAN_CANTEEN = 39  # 楠苑食堂
    NAN_MIX_BUILD = 40  # 楠苑综合楼
    STUDENT_HALL = 41  # 学生会堂

    # 学院楼
    BIO_ACADEMY = 42  # 生科院
    CHEMISTRY_ACADEMY = 43  # 化工学院
    SOFTWARE_ACADEMY = 44  # 软件学院
    PHYSICAL_ACADEMY = 45  # 物科学院
    SOURCE_ENVIR_ACADEMY = 46  # 资环学院
    ARCHITECTURE_ACADEMY = 47  # 城建学院
    INFO_ACADEMY = 48  # 信息学院
    ECONOMIC_ACADEMY = 49  # 经济学院
    LAW_ACADEMY = 50  # 法学院
    MOOT_COURT = 51  # 模拟法庭
    BUSINESS_ACADEMY = 52  # 商学院
    SPORT_ACADEMY = 53  # 体育学院
    ART_ACADEMY = 54  # 艺术学院
    NEWS_ACADEMY = 55  # 新闻学院
    ASTRONOMY_ACADEMY = 56  # 天文学院

    # 体育场
    INSTRUMENT_FIELD = 57  # 器械场地
    BADMINTON_GYM = 58  # 羽毛球馆
    FOOTBALL_FIELD = 59  # 足球场
    BASKETBALL_FIELD = 60  # 篮球场
    BASKETBALL_GYM = 61  # 篮球场
    TENNIS_FIELD = 62  # 网球场


class ApproximateNumber(Enum):
    """
    概数
    """
    RARELY = 1  # 很少
    LITTLE = 2  # 少
    ORDINARY = 3  # 一般
    MANY = 4  # 多
    PLENTY = 5  # 很多


Place = {
    Label.BUS_BASE.value: 0.08,
    Label.EXPERT_DORMITORY.value: 0.02,
    Label.SQUARE.value: 0.09,
    Label.ZE_LAKE.value: 0.13,
    Label.BELL_TOWER.value: 0.1,
    Label.INFO_TECH_CENTER.value: 0.05,
    Label.PALEON_INSTITUTE.value: 0.02,
    Label.MINGYUAN_BUILD.value: 0.04,
    Label.CENTENNIAL_HALL.value: 0.03,
    Label.EXPER_WASTE_CENTER.value: 0.02,
    Label.WEST_AUXILIARY_BUILD.value: 0.05,
    Label.EAST_AUXILIARY_BUILD.value: 0.06,
    Label.NAN_MIX_BUILD.value: 0.24,
    Label.STUDENT_HALL.value: 0.07,
}
