'''
스마트폰에서 스캔하면 연락처에 데이터가 입려되는 QR 코드 명함 이미지를 만든다.
'''


from pathlib import Path
import json
import streamlit as st
from PIL import Image, ImageDraw, ImageOps
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers.pil import RoundedModuleDrawer
from qrcode.image.styles.moduledrawers.pil import VerticalBarsDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import io


release_version = '2.2'

# 페이지 설정
st.set_page_config(
    page_title=f'QR {release_version}',
    page_icon='🔳',
    layout='wide',
)


def create_img_qr_code(
        type_box,
        size_box,
        thickness_border_in_box,
    ):
    '''
    qr code 이미지를 생성한다.
    '''

    qr_code = qrcode.QRCode(
        version=3,
        error_correction=qrcode.ERROR_CORRECT_H,
        box_size=size_box,
        border=thickness_border_in_box,
    )
    qr_code.add_data(vcard)
    qr_code.make(fit=True)

    if type_box == 'rounded square':
        img_qr_code = qr_code.make_image(image_factory=StyledPilImage, module_drawer=RoundedModuleDrawer()).convert('RGBA')   # 둥근 qr code
    elif type_box == 'vertical':
        img_qr_code = qr_code.make_image(image_factory=StyledPilImage, module_drawer=VerticalBarsDrawer()).convert('RGBA')   # 세로 줄 qr code
    else:
        img_qr_code = qr_code.make_image(fill_color='black', back_color='white').convert('RGBA')   # 일반 qr code

    return img_qr_code


def create_img_inner(
        img_inner,
        side_img_inner,
        thickness_frame,
        apply_mask=True,
    ):

    '''
    내부 이미지에 대한 처리를 한다.
        img_inner의 크기를 side_img_inner로 조정한다.
        img_inner에 원형 마스크를 적용한다.
        img_inner을 확장하여 흰색 배경을 추가한다.
    '''
    
    img_inner_copy = img_inner.convert('RGBA')
    width_img_inner, height_img_inner = img_inner_copy.size

    # 크기를 side_img_inner로 조정한다.
    side_longer_img_inner = max(width_img_inner, height_img_inner)
    if side_longer_img_inner > side_img_inner:
        scale = side_img_inner / side_longer_img_inner
        img_inner_copy = img_inner_copy.resize((int(width_img_inner * scale), int(height_img_inner * scale)))
        width_img_inner, height_img_inner = img_inner_copy.size

    if not apply_mask:
        return img_inner_copy
    
    # 원형의 마스크를 만든다.
    mask = Image.new('L', (width_img_inner, height_img_inner), 0)
    draw = ImageDraw.Draw(mask)
    circle_center = (width_img_inner // 2, height_img_inner // 2)
    circle_radius = min(width_img_inner, height_img_inner) // 2
    draw.ellipse(
        (
            circle_center[0] - circle_radius,
            circle_center[1] - circle_radius,
            circle_center[0] + circle_radius,
            circle_center[1] + circle_radius,
        ),
        fill=255,
    )

    # 마스크를 적용한다.
    img_inner_copy = Image.composite(
        img_inner_copy,
        Image.new('RGBA', img_inner_copy.size, (255, 255, 255, 255)),
        mask
    )

    # 테두리를 적용한다.
    img_inner_copy = ImageOps.expand(img_inner_copy, border=thickness_frame, fill='white')

    return img_inner_copy


def save_inputs_to_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def load_inputs_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_user_inputs():
    inputs = {
        'formatted_name': formatted_name,

        'name_prefix': name_prefix,
        'name_family': name_family,
        'name_middle': name_middle,
        'name_given': name_given,
        'name_suffix': name_suffix,
        
        'company': company,
        
        'type_url_1': type_url_1,
        'url_1': url_1,
        'type_url_2': type_url_2,
        'url_2': url_2,
        'type_url_3': type_url_3,
        'url_3': url_3,
        'type_url_4': type_url_4,
        'url_4': url_4,
        
        'type_email_1': type_email_1,
        'email_1': email_1,
        'type_email_2': type_email_2,
        'email_2': email_2,
        'type_email_3': type_email_3,
        'email_3': email_3,
        'type_email_4': type_email_4,
        'email_4': email_4,
        
        'tel_mobile': tel_mobile,
        'tel_office': tel_office,
        
        'note': note,
        
        'type_box': type_box,
        'size_box': size_box,
        'thickness_border_in_box': thickness_border_in_box,

        'use_img_inner': use_img_inner,
        'side_img_inner': side_img_inner,
        'thickness_frame': thickness_frame,
        'apply_mask': apply_mask,
        'x_img_inner': x_img_inner,
        'y_img_inner': y_img_inner,
    }
    return inputs


def set_user_inputs(data):
    global formatted_name, name_prefix, name_family, name_middle, name_given, name_suffix, company
    global type_url_1, url_1, type_url_2, url_2, type_url_3, url_3, type_url_4, url_4
    global type_email_1, email_1, type_email_2, email_2, type_email_3, email_3, type_email_4, email_4
    global tel_mobile, tel_office, note, type_box, size_box, thickness_border_in_box
    global use_img_inner, img_inner, side_img_inner, thickness_frame, apply_mask, x_img_inner, y_img_inner, path_img_inner

    formatted_name = data['formatted_name']

    name_prefix = data['name_prefix']
    name_family = data['name_family']
    name_middle = data['name_middle']
    name_given = data['name_given']
    name_suffix = data['name_suffix']

    company = data['company']
    
    type_url_1 = data['type_url_1']
    url_1 = data['url_1']
    type_url_2 = data['type_url_2']
    url_2 = data['url_2']
    type_url_3 = data['type_url_3']
    url_3 = data['url_3']
    type_url_4 = data['type_url_4']
    url_4 = data['url_4']
    
    type_email_1 = data['type_email_1']
    email_1 = data['email_1']
    type_email_2 = data['type_email_2']
    email_2 = data['email_2']
    type_email_3 = data['type_email_3']
    email_3 = data['email_3']
    type_email_4 = data['type_email_4']
    email_4 = data['email_4']
    
    tel_mobile = data['tel_mobile']
    tel_office = data['tel_office']

    note = data['note']
    
    type_box = data['type_box']
    size_box = data['size_box']
    thickness_border_in_box = data['thickness_border_in_box']

    use_img_inner = data['use_img_inner']
    side_img_inner = data['side_img_inner']
    thickness_frame = data['thickness_frame']
    apply_mask = data['apply_mask']
    x_img_inner = data['x_img_inner']
    y_img_inner = data['y_img_inner']


def process_button_create_qr_code_clicked():

    # qr 코드 이미지를 생성한다.
    img_qr_code = create_img_qr_code(
        type_box=type_box,
        size_box=size_box,
        thickness_border_in_box=thickness_border_in_box,
    )    


    # inner image가 있을 때만 실행한다.
    if use_img_inner and img_inner:
        # inner image를 생성한다.
        img_inner_copy = create_img_inner(
            img_inner=img_inner,
            side_img_inner=side_img_inner,
            thickness_frame=thickness_frame,
            apply_mask=apply_mask,
        )

        # qr 코드 이미지에 inner image를 넣는다.
        x_pos = img_qr_code.width - side_img_inner - thickness_frame - x_img_inner
        y_pos = img_qr_code.height - side_img_inner - thickness_frame - y_img_inner

        img_qr_code.paste(
            img_inner_copy,
            (x_pos, y_pos),
            mask=img_inner_copy.split()[3],
        )


    # qr 코드 이미지를 출력한다.
    with col_qr_code:
        st.image(img_qr_code)
        st.write(f'QR 코드 크기 = {img_qr_code.size}')
        if path_img_inner:
            st.write(f'이미지 위치: {x_pos=}, {y_pos=}')

        img_byte_arr = io.BytesIO()
        img_qr_code.save(img_byte_arr, format='PNG')
        img_byte_arr = img_byte_arr.getvalue()

        # qr 코드 이미지 다운로드
        button_download_qr_img_clicked = st.download_button(
            label='다운로드 QR 코드 이미지',
            data=img_byte_arr,
            file_name=f'{formatted_name}_{company}_{type_box}_{size_box}_{thickness_border_in_box}_{side_img_inner}_{thickness_frame}_{x_img_inner}_{y_img_inner}.png',
            mime='image/png',
            key='download_qr_img',
            use_container_width=True,
        )



if __name__ == '__main__':

    # default user inputs
    dir_json = Path('json_user_inputs')
    dir_json.mkdir(exist_ok=True)

    if 'user_inputs' not in st.session_state:
        first_run = True
        user_inputs = load_inputs_from_json(dir_json/'default_user_inputs.json')
        set_user_inputs(user_inputs)
        path_img_inner = 'img_inner/cat.png'
        img_inner = Image.open(path_img_inner)
        st.session_state.user_inputs = user_inputs
    else:
        first_run = False
        user_inputs = st.session_state.user_inputs
        set_user_inputs(user_inputs)

        path_img_inner = st.session_state.path_img_inner
        img_inner = st.session_state.img_inner


    st.title(f'QR 코드 명함 생성기 {release_version}')
    st.write('- 스마트폰 카메라로 QR 코드를 스캔하면 연락처 앱에 데이터가 자동으로 입력되는 QR 코드 이미지를 만듭니다.')
    st.write('- 종이 명함 대신 사용되어 환경에 도움이 되면 좋겠습니다.')
    st.write('- 간략 사용법: 명함 데이터를 입력하고 "QR 코드 생성" 버튼을 클릭하세요. 이미지를 다운로드 받으세요.')
    st.write('- 상세 사용법: https://github.com/hsl38/qr_vcard')
    st.divider()


    # 페이지 레이아웃
    col_vcard, col_para, col_qr_code = st.columns([5, 3, 3])

    def update_vcard_inputs():
        global formatted_name, name_prefix, name_family, name_middle, name_given, name_suffix, company
        global type_url_1, url_1, type_url_2, url_2, type_url_3, url_3, type_url_4, url_4
        global type_email_1, email_1, type_email_2, email_2, type_email_3, email_3, type_email_4, email_4
        global tel_mobile, tel_office, note, vcard, vcard_text

        # vcard 정보 입력
        with col_vcard:
            # formmated name
            formatted_name = st.text_input('표시할 이름', formatted_name)

            # name. 5개 필드로 구성된다.
            col_names = st.columns(5)
            name_prefix = col_names[0].text_input('Dr./Prof./Mr./Ms.', name_prefix)
            name_family = col_names[1].text_input('성 (Family Name)', name_family)
            name_middle = col_names[2].text_input('Middle Name', name_middle)
            name_given = col_names[3].text_input('이름 (Given Name)', name_given) 
            name_suffix = col_names[4].text_input('직급', name_suffix)

            # company
            company = st.text_input('회사명', company)

            # url of company
            col_url_email = st.columns(2)
            with col_url_email[0].container(border=True):
                type_url_1 = st.text_input('URL 1 제목', company)
                url_1 = st.text_input('URL 1', url_1)

            # 사용자가 지정한 url
            with col_url_email[0].container(border=True):
                type_url_2 = st.text_input('URL 2 제목', type_url_2)
                url_2 = st.text_input('URL 2', url_2)

            # 사용자가 지정한 url
            with col_url_email[0].container(border=True):
                type_url_3 = st.text_input('URL 3 제목', type_url_3)
                url_3 = st.text_input('URL 3', url_3)

            # 사용자가 지정한 url
            with col_url_email[0].container(border=True):
                type_url_4 = st.text_input('URL 4 제목', type_url_4)
                url_4 = st.text_input('URL 4', url_4)


            # email of company
            with col_url_email[1].container(border=True):
                type_email_1 = st.text_input('이메일 1 제목', company)
                email_1 = st.text_input('이메일 1', email_1)

            # 사용자가 지정한 email
            with col_url_email[1].container(border=True):
                type_email_2 = st.text_input('이메일 2 제목', type_email_2)
                email_2 = st.text_input('이메일 2', email_2)

            # 사용자가 지정한 email
            with col_url_email[1].container(border=True):
                type_email_3 = st.text_input('이메일 3 제목', type_email_3)
                email_3 = st.text_input('이메일 3', email_3)

            # 사용자가 지정한 email
            with col_url_email[1].container(border=True):
                type_email_4 = st.text_input('이메일 4 제목', type_email_4)
                email_4 = st.text_input('이메일 4', email_4)

            # 전화번호
            col_tel = st.columns(2)
            tel_mobile = col_tel[0].text_input('모바일 전화번호', tel_mobile)
            tel_office = col_tel[1].text_input('사무실 전화번호', tel_office)

            # note
            note = st.text_area('노트 (줄바꿈 없이 한 줄로 입력하세요. 첫 줄만 표시됩니다.)', note)

            # vcard
            vcard = f'BEGIN:VCARD\nVERSION:3.0'

            if name_prefix or name_family or name_middle or name_given or name_suffix:
                vcard += f'\nN:{name_family};{name_given};{name_middle};{name_prefix};{name_suffix}'
            
            if formatted_name:
                vcard += f'\nFN:{formatted_name}'

            if company:
                vcard += f'\nORG:{company}'

            if type_url_1 or url_1:
                vcard += f'\nURL;TYPE={type_url_1}:{url_1}'
            if type_url_2 or url_2:
                vcard += f'\nURL;TYPE={type_url_2}:{url_2}'
            if type_url_3 or url_3:
                vcard += f'\nURL;TYPE={type_url_3}:{url_3}'
            if type_url_4 or url_4:
                vcard += f'\nURL;TYPE={type_url_4}:{url_4}'

            if type_email_1 or email_1:
                vcard += f'\nEMAIL;TYPE={type_email_1}:{email_1}'
            if type_email_2 or email_2:
                vcard += f'\nEMAIL;TYPE={type_email_2}:{email_2}'
            if type_email_3 or email_3:
                vcard += f'\nEMAIL;TYPE={type_email_3}:{email_3}'
            if type_email_4 or email_4:
                vcard += f'\nEMAIL;TYPE={type_email_4}:{email_4}'

            if tel_mobile:
                vcard += f'\nTEL;TYPE=mobile,pref:{tel_mobile}'

            if tel_office:
                vcard += f'\nTEL;TYPE=office:{tel_office}'

            if note:
                vcard += f'\nNOTE:{note}'

            vcard += '\nEND:VCARD'

            vcard_text = st.text_area('vcard', vcard, height=400)

    update_vcard_inputs()

    # qr code 생성 파라미터 입력
    with col_para:

        # inner image
        use_img_inner = st.checkbox('이미지 적용', value=True)


        placeholder_img_inner = st.empty()
        placeholder_img_inner_size = st.empty()

        # path_img_inner_prev = path_img_inner

        print(f'before: {path_img_inner = }')
        file_uploaded = st.file_uploader(
            '이미지 파일 업로드드', 
            type=['png', 'jpg', 'jpeg'], 
            key='inner_img', 
            disabled=(not use_img_inner)
        )
        print(f'after: {type(path_img_inner) = }')

        if file_uploaded is not None:
            placeholder_img_inner.image(file_uploaded, width=100)
            print(f'image file_uploaded: {type(file_uploaded) = }')
            img_inner = Image.open(file_uploaded)
            st.session_state.img_inner = img_inner
            st.session_state.path_img_inner = path_img_inner

        if img_inner:
            placeholder_img_inner.image(img_inner, width=100)
            width_img_inner, height_img_inner = img_inner.size
            placeholder_img_inner_size.text(f'이미지 크기 = {width_img_inner} x {height_img_inner}')
            

        with st.form('qr_code_para'):
            button_create_qr_code_clicked = st.form_submit_button('QR 코드 생성', type='primary', use_container_width=True)

            col_para_1, col_para_2 = st.columns(2)
            # qr code 종류
            types_box = ['rounded square', 'vertical', 'standard']
            type_box = col_para_1.selectbox('QR 코드 종류', types_box, index=1, help='QR 코드의 점 모양과 점들의 연결 형식에 따른 종류를 선택합니다.')

            # qr code 박스(픽셀,  도트) 크기
            size_box = col_para_2.number_input('점 크기', value=4, min_value=1, max_value=8, help='QR 코드 한 점의 크기를 지정합니다.')

            # qr code 테두리 굵기. 박스 크기의 몇 배로 할 것인가.
            thickness_border_in_box = st.number_input('QR 코드 테두리 [점 크기의 배수]', value=4, min_value=1, max_value=8, help='QR 코드의 테두리의 폭을 지정합니다.')

            col_para_3, col_para_4 = st.columns(2)
            # inner image 크기
            # inner image가 있을 때만 입력할 수 있다.
            # 박스 크기의 16배로 하는 것이 기본값이다.
            # 너무 크면 qr 코드 영역이 작아 코드가 읽어지지 않는다.
            # inner image는 오른쪽 아래에 위치한다.
            side_img_inner = col_para_3.number_input('이미지 크기', value=size_box * 16, min_value=32, max_value=128, disabled=(not use_img_inner), help='이미지의 크기를 지정합니다. 이미지가 너무 크면 QR 코드가 읽히지 않을 수 있습니다.')
            thickness_frame =col_para_4.number_input('이미지 테두리', value=2, min_value=0, max_value=8, disabled=(not use_img_inner), help='이미지의 테두리 폭을 지정합니다.')
    
            x_img_inner = col_para_3.number_input('이미지 수평 이동', value=size_box * 6, min_value=0, max_value=640, step=size_box, disabled=(not use_img_inner), help='값을 키우면 이미지가 왼쪽으로 이동합니다.')
            y_img_inner = col_para_4.number_input('이미지 수직 이동', value=size_box * 6, min_value=0, max_value=640, step=size_box, disabled=(not use_img_inner), help='값을 키우면 이미지가 위로 이동합니다.')

            apply_mask = st.checkbox('마스크 적용', value=True, disabled=(not use_img_inner), help='이미지에 원형 마스크 적용 여부를 지정합니다.')

        # download user inputs
        user_inputs = get_user_inputs()
        json_data = json.dumps(user_inputs, ensure_ascii=False, indent=4)
        button_download_clicked = st.download_button(
            label='입력 데이터 다운로드',
            data=json_data,
            file_name='user_inputs.json',
            mime='application/json',
            key='download_user_inputs',
            help='다음에 사용할 수 있도록 화면 왼쪽에 입력한 데이터를 다운로드 받습니다.',
            use_container_width=True,
        )
        print(f'download user inputs: {path_img_inner = }')


        # user input json을 로드한다.
        json_user_input = st.file_uploader(
            '입력 데이터 업로드', 
            type='json', 
            key='json_user_input',
            help='전에 다운로드 받았던 입력 데이터 파일을 업로드하여 데이터를 입력할 수 있습니다.'
        )
        if json_user_input is not None:
            user_inputs = json.load(json_user_input)

            set_user_inputs(user_inputs)
            st.session_state.user_inputs = user_inputs
            st.session_state.img_inner = img_inner

            st.success('QR 코드 생성 버튼을 클릭하면 파일의 데이터가 적용됩니다.')
            print(f'upload not None {user_inputs = }')



    # qr 코드 생성
    if button_create_qr_code_clicked:
        process_button_create_qr_code_clicked()

    # 자동 QR 코드 생성 (처음 실행할 때만)
    if first_run:
        path_img_inner = 'img_inner/cat.png'
        img_inner = Image.open(path_img_inner)
        st.session_state.img_inner = img_inner
        st.session_state.path_img_inner = path_img_inner

        process_button_create_qr_code_clicked()


