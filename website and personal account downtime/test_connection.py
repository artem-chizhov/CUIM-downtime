from requests_html import HTMLSession
import os
import dotenv


session = HTMLSession()


def session_param(url, log, pas):

    session.post(url, {
        'name': log,
        'password': pas,
        'autologin': 1,
        'enter': 'Sign in'
    })


def link(url, idx):
    var = f'{url}history.php?itemids%5B0%5D={idx}&action=showvalues&plaintext=Как простой текст&idx=web.item.graph.filter'
    return var


def check_url(url, log, pas, idx):
    try:
        session_param(url=url, log=log, pas=pas)
        result = session.get(link(url=url, idx=idx))
        result_html = result.html.find('main', first=True)
        text = str(result_html.text[0:18])

        if text == 'You are not logged':
            return [False, result.status_code, 'Ошибка авторизации']
        elif result.status_code != 200:
            return [False, result.status_code, result.status_code]
        else:
            return [True, result.status_code, 'Connection is OK']
    except Exception as err:
        return [False, 'Не корректная ссылка!', err]


def check_all():

    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)

    msk = check_url(url=os.environ.get('URL_MSK'),
                    idx=os.environ.get('IDX2_MSK_SITE'),
                    log=os.environ.get('LOGIN_MSK'),
                    pas=os.environ.get('PASSWORD_MSK'))

    spb = check_url(url=os.environ.get('URL_SPB'),
                    idx=os.environ.get('IDX2_SPB_SITE'),
                    log=os.environ.get('LOGIN_SPB'),
                    pas=os.environ.get('PASSWORD_SPB'))

    ural = check_url(url=os.environ.get('URL_URAL'),
                     idx=os.environ.get('IDX2_URAL_SITE'),
                     log=os.environ.get('LOGIN_URAL'),
                     pas=os.environ.get('PASSWORD_URAL'))

    return {'msk': msk, 'spb': spb, 'ural': ural}
