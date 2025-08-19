from xinshili.dxm_xyl_yd_tack import auto
from xinshili.utils import get_computer_model


def call3():
    if "MacBookPro" in get_computer_model():
        dxm_xyl_tk = "/Users/zkp/Desktop/B&Y/轨迹统计/dxm_xyl_track"
    else:
        dxm_xyl_tk = "/Volumes/B&Y/轨迹统计/dxm_xyl_track/"

    auto(dxm_xyl_tk, False)


if __name__ == '__main__':
    call3()
