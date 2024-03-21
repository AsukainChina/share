from speedtest import Speedtest
from ping3 import ping
from time import sleep
from multiprocessing import Process


def network_speed():
    wrong_server_list = []
    wrong_server_number = -1
    # 将wrong_server_number初始值设定为-1就对了，开始运行时，wrong_server_list没有故障网址但是发生故障，因此第一次显示的网络故障数为2

    # print("准备测试网络速度...")
    while True:
        try:
            st = Speedtest()
            break
        except Exception as e:
            print(type(e).__name__, ":", e)

    # print("寻找合适网站中...")
    while True:
        try:
            best_server = st.get_best_server()
            urllib = best_server["url"]
            wrong_server_number += 1
            for _ in wrong_server_list:
                print(f"服务器故障，目前记录的服务器故障次数为{wrong_server_number}次")
                break
            wrong_server_list.append(urllib)
            print(f"测速中...\n目标网址{urllib}")
            st.download()
            st.upload()
            st.results.share()
            break
        except TimeoutError:
            print("寻找服务器超时")
            sleep(1)
            print("重新寻找合适网站中...")
            continue
        except Exception as e:
            print(type(e).__name__, ":", e)
            sleep(1)
            print("重新寻找合适网站中...")
            continue

    results_dict = st.results.dict()

    download_speed = results_dict['download'] / (10 ** 6)
    upload_speed = results_dict['upload'] / (10 ** 6)

    print(f'下载速度: {download_speed} Mbps')
    print(f'上传速度: {upload_speed} Mbps')


def ping_test():
    print("准备测试网络延迟，目标网站：baidu.com")
    all_time_ping_in_ms = 0
    test_time = []
    count = 20
    interrupt = 0

    for _ in range(20):
        try:
            ping_time = ping("baidu.com")
            ping_time_in_ms = 1000 * ping_time
            if ping_time_in_ms == 0:
                print("网络中断")
                count -= 1
            else:
                print(f"网络延迟{str(round(ping_time_in_ms, 2))}ms")
                test_time.append(ping_time_in_ms)
                all_time_ping_in_ms += ping_time_in_ms
            sleep(0.5)
        except TypeError:
            print("网络中断")
            interrupt += 1
        except Exception as e:
            print(type(e).__name__, ":", e)
            interrupt += 1

    if interrupt != 20:
        try:
            print(f"\n平均时间{str(round(all_time_ping_in_ms / count, 2))}ms")
            print(f"最长时间{str(round(max(test_time), 2))}ms")
            print(f"最短时间{str(round(min(test_time), 2))}ms")
            print(f"丢包率{str(round(interrupt / 20 * 100, 2))}%")
            print("正在测速中")
        except Exception as e:
            print(type(e).__name__, ":", e)
    else:
        words_lost_connection()


def words_lost_connection():
    print("您的网络故障，测试中有效ping值数据个数为0，无法计算平均ping值")
    sleep(0.5)
    print("您的网络故障，测试中有效ping值数据个数为0，无法计算最长时间")
    sleep(0.5)
    print("您的网络故障，测试中有效ping值数据个数为0，无法计算最短时间")
    sleep(0.5)
    print("您的丢包率为——100%")


def count_down():
    input("按任意键关闭程序并进入倒计时")

    def time_sleep(data):
        for t in range(data, -1, -1):
            my_str = f"程序关闭倒计时:{t + 1}S"
            print(f"\r{my_str} ", end="", flush=True)
            sleep(1)

    if __name__ == '__main__':
        time_sleep(4)


def do_everything():
    def main():
        process1 = Process(target=ping_test)
        process1.start()
        sleep(5)
        process2 = Process(target=network_speed)
        process2.start()
        process1.join()
        process2.join()

    if __name__ == '__main__':
        main()


do_everything()
count_down()
