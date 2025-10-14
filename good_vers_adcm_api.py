import requests
import time

# Данные ADCM
url_adcm = "adhadm-04-adcm"
user_adcm = "admin"
pass_adcm = "admin"

# Указываем список хостов для добавления
list_of_hosts = [
    "139.28.221.24",
    "adhadm-111-mnode01.ru-central1.internal",
]

# Указываем пользователя для подключения к хостам
user_host = "root"
# Здесь указываем содержимое приватного ключа хоста на котором расположен ADCM,
# содержимое обернуто в три одинарные кавычки, должны быть на той же строке, что и ключ
private_key = """-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAABlwAAAAdzc2gtcn
NhAAAAAwEAAQAAAYEAm/rUQh7Bbf7N9EXEGbOKf4PGJv8GFkaR2qCkAS4fUVrWQx2cj1D6
WiL3vQMjuwpxwWErH4CTPO0hj6R3YMJJC4z8N+yRW8sk8IdhSspyOlDYL4owBPy/Q6uzIO
tolrxRCV4YyCKkXEeyLMchiAmI14Jwa7zoHzrdYcuRmA84cKBqmv48pd6IPlwDmufXXHCx
OSrfXZQgYkSvQwwjJ1q1rv1umHcPdBGkS88oSenmW7ZbzVI4UdBTrjZDQrpZLrBBeqQuox
HSDRtiPaLVRTNr0sFUjt0tXZyM07OOTSifz21OBRvzn2prfBVGrsV7IyJRt6MN1Uc8HHJZ
c0L0Hh+Ug7V+uZW9w2PmbKGlbNq1bkhzzK1MX9hq4T6mZWrpkVQXAofF5/hN8wTIDo5Op9
WR5mP/nLwRIOhd4cR2P5bjB+j4/2tNxCV9g65TZhtj4K9xF3zRpt8hJzF80l2oP1N2V6nR
GmF+71+TmhOVM36F642GcB5DHlCMa23IpAiNq/HpAAAFkNo7DX/aOw1/AAAAB3NzaC1yc2
EAAAGBAJv61EIewW3+zfRFxBmzin+Dxib/BhZGkdqgpAEuH1Fa1kMdnI9Q+loi970DI7sK
ccFhKx+AkzztIY+kd2DCSQuM/DfskVvLJPCHYUrKcjpQ2C+KMAT8v0OrsyDraJa8UQleGM
gipFxHsizHIYgJiNeCcGu86B863WHLkZgPOHCgapr+PKXeiD5cA5rn11xwsTkq312UIGJE
r0MMIydata79bph3D3QRpEvPKEnp5lu2W81SOFHQU642Q0K6WS6wQXqkLqMR0g0bYj2i1U
Uza9LBVI7dLV2cjNOzjk0on89tTgUb859qa3wVRq7FeyMiUbejDdVHPBxyWXNC9B4flIO1
frmVvcNj5myhpWzatW5Ic8ytTF/YauE+pmVq6ZFUFwKHxef4TfMEyA6OTqfVkeZj/5y8ES
DoXeHEdj+W4wfo+P9rTcQlfYOuU2YbY+CvcRd80abfIScxfNJdqD9Tdlep0Rphfu9fk5oT
lTN+heuNhnAeQx5QjGttyKQIjavx6QAAAAMBAAEAAAGABE01sRieykEojiPl6XUKfOOGEZ
F/KhpaX6KGP1uVpMVZ6xosFQY9T0LPXPyzDa+XLUd4HFtsBBZAkpDtM2OMRuellYe+Rv8q
VsFPCTRd09airaX0ltCfGDdKHn5rgRuyquzXx14wNPTLuMEpnzIvHk1kOw5nwuO5Uv79lg
lWa8G6yuk3xDXHwVuBhHJAHdYkRxCz/gVNotQk1rclGYref5PQ6t6+s/tgEfClumsbTZxw
+e+6aqQxiJiJwJN5zegxrRGJVF9AEGmDqzXORK17QOoThazTRTmIufo34arxXJcbb1mpK5
8aVXksySlC2sRkgs4Kt+znHmamvYJw8CFTKMVZUT0u2KpxCLDtXiFHsOLb9uWYmHBMTPes
w6kFFIf9wheqrz/Q+Fp/T3Nd90UG5pGCrlNOfyPbXE8BSn0CWdhT/JWlEjqpwgzBJp3CE0
l1vtDCsKqh8tmZIVGTtlTo5fcSKB7BQUY2j+IA0lCudpA3n4MFCbhR1LqFOjp2opvhAAAA
wGeZ1crV7zM0wQhCVbOSDWGxPgX2/AZnA6wAKDzGcAHizVzCXQV3vxOqdYYG3uSRS7pc1W
JFansP0wzB7UJu+S/sYdoibBAqcyhNZWoPJ/PBoa+QZEER2kxn4urokvOfbbzpcDlHZkJD
/4fSmAseWvReouNJOKdK+hvN31PA51jkRu8hUnn8IR4jeffwMS5FCfdy/2trbyThS5BSEa
OiK2xMNC3ig0d+SwcUVIYG3m+3XgFdOaSrSptltQ7QC9XFDgAAAMEAxFddqGpN6/AMvQAv
Eqdj0DiK+fSHomFwNgWKsWA/Yj0LASLGyRYWsX7l8hmKWV30pQ9Ssn+pt+XoeRpmSn28H7
pB2ndh4/JSch7lqLEJpq8pUhXjblTelTSfTjrg6TBqZd5dowOpnYAtzU5KWpyGWZA7YxX2
PY6yJFr6RPMwBrTX5yenF+EZaKrRV4PwKwXkqMJpFuBomaKIndQZ5IA3lkNawxKcY3wR1T
AE+HmLVu8MQ+pu7vd+oEUrMESpUbxJAAAAwQDLX+Y4fMjkMvQXheGZ0lk4iqxVGl8UlN3U
3/H0cKSfVYuhdy4toXGfVQ/db/iA7ZhW5ON0j4LE5cweYBXGbBqzZ+rv3iFBJ0tDFwow4y
0p6Kq9yr0OWmKHNqpJDvY36dfoOHq/cLl8R4OU8/eI1l4PijOLJdaNrXzDHU1hO/OdMmHx
mFk6+TvwBgv/xHwT64OBaAZzTV50F3bPkghSRiMipEoWGDYO0sx0MmlJe/Q5n75JpMyFId
d8G63CR1HQSKEAAAAUYWRtaW5AYWRoYWRtLTA0LWFkY20BAgMEBQYH
-----END OPENSSH PRIVATE KEY-----"""


class color:
    PURPLE = "\033[1;35;48m"
    CYAN = "\033[1;36;48m"
    BOLD = "\033[1;37;48m"
    BLUE = "\033[1;34;48m"
    GREEN = "\033[1;32;48m"
    YELLOW = "\033[1;33;48m"
    RED = "\033[1;31;48m"
    BLACK = "\033[1;30;48m"
    UNDERLINE = "\033[4;37;48m"
    END = "\033[1;37;0m"


# Получение токена
def get_adcm_token():
    response = requests.post(
        f"http://{url_adcm}:8000/api/v2/token/",
        data={"username": user_adcm, "password": pass_adcm},
    )
    response.raise_for_status()
    token = response.json().get("token")
    if not token:
        raise Exception("Не удалось получить токен")
    print(f"Token: {token}")
    return token


# Получение id прототипа хоста
def get_prototype_id(headers):
    response = requests.get(
        f"http://{url_adcm}:8000/api/v2/prototypes/?type=host", headers=headers
    )
    response.raise_for_status()
    host_prototype_data = response.json()
    host_prototype_id = (
        host_prototype_data["results"][0]["id"]
        if "results" in host_prototype_data
        else None
    )
    if not host_prototype_id:
        raise Exception("Failed to obtain host prototype ID")
    # print(f"Host Prototype ID: {host_prototype_id}")
    return host_prototype_id


# Получение id провайдера
def get_provider_id(headers):
    response = requests.get(
        f"http://{url_adcm}:8000/api/v2/hostproviders/", headers=headers
    )
    response.raise_for_status()
    provider_data = response.json()
    provider_id = (
        provider_data["results"][0]["id"] if "results" in provider_data else None
    )
    if not provider_id:
        raise Exception("Failed to obtain provider ID")
    # print(f"Provider ID: {provider_id}")
    return provider_id


# Создание хоста
def hosts_create(headers, host_prototype_id, provider_id, host):
    response = requests.post(
        f"http://{url_adcm}:8000/api/v2/hosts/",
        headers=headers,
        json={
            "fqdn": host,
            "name": host,  # Используем полное FQDN в качестве имени
            "prototype_id": host_prototype_id,
            "hostprovider_id": provider_id,  # Поправляем поле на hostprovider_id
        },
    )
    if response.status_code == 201:
        print(f"{color.GREEN}Хост {host} успешно создан{color.END}")
        host_id = response.json()["id"]
    else:
        print(f"{color.RED}Хост {host} не создался: {response.json()}{color.END}")
    return host_id


# Настройка конфигурации хоста
def hosts_configuration(headers, host_id, host):
    url_host_config = f"http://{url_adcm}:8000/api/v2/hosts/{host_id}/configs/"
    config_data = {
        "config": {
            "__main_info": "Please configure <b>Connection address</b> (if DNS not works),<b>Username</b>, <b>Password</b> or <b>SSH private key</b> (if use instead ofpassword). And do not forget to run <b>Install statuschecker</b> action.\n",
            "ansible_user": user_host,
            "ansible_ssh_pass": None,
            "ansible_host": host,
            "ansible_become": True,
            "ansible_ssh_port": "22",
            "ansible_ssh_private_key_file": private_key,
            "ansible_ssh_common_args": "-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null",
            "ansible_become_pass": None,
        },
        "attr": {},
        "adcm_meta": {},
    }
    response = requests.post(url_host_config, headers=headers, json=config_data)
    if response.status_code == 201:
        print(f"{color.GREEN}{host} успешно сконфигурирован{color.END}")
        result = "success"
    else:
        print(
            f"{color.RED}Для {host} не удалось задать конфигурацию: {response.json()}{color.END}"
        )
        result = "failed"
    return result


def get_and_run_task_host(headers, host_id, task_name):
    url_get_host_actions = f"http://{url_adcm}:8000/api/v2/hosts/{host_id}/actions/"
    response_actions = requests.get(url_get_host_actions, headers=headers)
    action_id = next(
        (
            item["id"]
            for item in response_actions.json()
            if item["displayName"] == task_name
        ),
        None,
    )
    url_run_host_task = (
        f"http://{url_adcm}:8000/api/v2/hosts/{host_id}/actions/{action_id}/run/"
    )
    response = requests.post(url_run_host_task, headers=headers)
    # print(response.json())
    if response.status_code == 200:
        task_id = response.json()["id"]
    else:
        print(f"{color.RED}При запуске {task_name} произошла ошибка{color.END}")
        task_id = "error"
    return task_id


def check_task_status(headers, task_id):
    url_host_check_connection_task = f"http://{url_adcm}:8000/api/v2/tasks/{task_id}/"
    while True:
        try:
            response = requests.get(url_host_check_connection_task, headers=headers)
            response_task = response.json()["status"]
            response_task_name = response.json()["displayName"]
            response_task_name_host = response.json()["objects"][1]["name"]
            # Проверяем статус ответа
            if response_task == "success":
                print(
                    f"{color.GREEN}Статус таски {response_task_name} для хоста {response_task_name_host}: Успех{color.END}"
                )
                result = response.json()["objects"][1]["id"]
                return result
            elif response_task == "failed":
                print(
                    f"{color.RED}Статус таски {response_task_name} для хоста {response_task_name_host}: Ошибка{color.END}"
                )
                break
            # Пауза перед следующей попыткой (чтобы не перегружать сервер)
            time.sleep(5)  # Можно поменять интервал ожидания по желанию

        except Exception as e:
            print(f"Произошла ошибка: {e}{color.END}")
            break


token = get_adcm_token()
headers = {"Authorization": f"Token {token}", "Content-Type": "application/json"}

host_prototype_id = get_prototype_id(headers)
provider_id = get_provider_id(headers)
list_of_task = []
for host in list_of_hosts:
    host_id = hosts_create(headers, host_prototype_id, provider_id, host)
    config = hosts_configuration(headers, host_id, host)
    if config == "success":
        task_name_connection = "Check connection"
        task = get_and_run_task_host(headers, host_id, task_name_connection)
        list_of_task.append(task)
        print(
            f"{color.YELLOW}Запустили Check connection для {host} ожидаем завершения{color.END}"
        )

success_hosts = []
for task_id in list_of_task:
    success_hosts.append(check_task_status(headers, task_id))

list_of_task.clear()


for success_host in success_hosts:
    if success_host != None:
        task_name_statuschecker = "Install statuschecker"
        task_install_statuschecker = get_and_run_task_host(
            headers, success_host, task_name_statuschecker
        )
        list_of_task.append(task_install_statuschecker)
        print(
            f"{color.YELLOW}Запустили Install statuschecker для хостов, которые успешно прошли Check connection ожидаем завершения{color.END}"
        )

for task_id in list_of_task:
    success_hosts = check_task_status(headers, task_id)
