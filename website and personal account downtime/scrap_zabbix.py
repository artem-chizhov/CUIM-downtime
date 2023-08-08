from requests_html import HTMLSession
import os
import dotenv

dotenv.load_dotenv()

login_msk = os.getenv("LOGIN_MSK")
login_spb = os.getenv("LOGIN_SPB")
login_ural = os.getenv("LOGIN_URAL")
pass_msk = os.getenv("PASSWORD_MSK")
pass_spb = os.getenv("PASSWORD_SPB")
pass_ural = os.getenv("PASSWORD_URAL")
idx_msk_lk = os.getenv("IDX2_MSK_LK")
idx_spb_lk = os.getenv("IDX2_SPB_LK")
idx_ural_lk = os.getenv("IDX2_URAL_LK")
idx_msk_site = os.getenv("IDX2_MSK_SITE")
idx_spb_site = os.getenv("IDX2_SPB_SITE")
idx_ural_site = os.getenv("IDX2_URAL_SITE")
url_msk = os.getenv("URL_MSK")
url_spb = os.getenv("URL_SPB")
url_ural = os.getenv("URL_URAL")

session = HTMLSession()


def session_param(url, log, pas):

    session.post(url, {
                'name': log,
                'password': pas,
                'autologin': 1,
                'enter': 'Sign in'
                })

def link(url, idx, date1, date2):
    var = f'{url}history.php?itemids%5B0%5D={idx}&action=showvalues&plaintext=Как простой текст&idx=web.item.graph.filter&from={date1}&to={date2}'
    return var

def scrap_data(date1, date2, url, login, password, idx):

    session_param(url=url, log=login, pas=password)
    result = session.get(link(url=url, idx=idx, date1=date1, date2=date2))
    result = result.html.find('pre', first=True)
    return result.text

def listmerge(lists_slist):
    result_list=[]
    for lst in lists_slist:
        result_list.extend(lst)
    return result_list

def start_receiving(time_list):
    finish_data_dict = {
                        'msk_site':[],
                        'spb_site':[],
                        'ural_site':[],
                        'msk_lk':[],
                        'spb_lk':[],
                        'ural_lk':[]
                        }

    for idx, val in enumerate(time_list):
        if idx + 1 == len(time_list):
            break

        site_msk = scrap_data(date1=val,date2=time_list[idx + 1],
                              url=url_msk,
                              idx=idx_msk_site,
                              login=login_msk,
                              password=pass_msk)
        site_spb = scrap_data(date1=val,date2=time_list[idx + 1],
                              url=url_spb,
                              idx=idx_spb_site,
                              login=login_spb,
                              password=pass_spb)
        site_ural = scrap_data(date1=val,date2=time_list[idx + 1],
                               url=url_ural,
                               idx=idx_ural_site,
                               login=login_ural,
                               password=pass_ural)
        
        finish_data_dict['msk_site'].append(site_msk.split('\n'))
        finish_data_dict['spb_site'].append(site_spb.split('\n'))
        finish_data_dict['ural_site'].append(site_ural.split('\n'))

        lk_msk = scrap_data(date1=val,date2=time_list[idx + 1],
                            url=url_msk,
                            idx=idx_msk_lk,
                            login=login_msk,
                            password=pass_msk)
        lk_spb = scrap_data(date1=val,date2=time_list[idx + 1],
                            url=url_spb,
                            idx=idx_spb_lk,
                            login=login_spb,
                            password=pass_spb)
        lk_ural = scrap_data(date1=val,date2=time_list[idx + 1],
                             url=url_ural,
                             idx=idx_ural_lk,
                             login=login_ural,
                             password=pass_ural)
        
        finish_data_dict['msk_lk'].append(lk_msk.split('\n'))
        finish_data_dict['spb_lk'].append(lk_spb.split('\n'))
        finish_data_dict['ural_lk'].append(lk_ural.split('\n'))

    for key,val in finish_data_dict.items():
        finish_data_dict[key] = listmerge(val)

    return finish_data_dict
