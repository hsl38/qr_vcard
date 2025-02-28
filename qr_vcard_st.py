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


release_version = '2.1'

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
    Create QR code image from content to output path with a inner imgage
    '''

    # qr code 이미지를 생성한다.
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
        path_img_inner,
        side_img_inner,
        thickness_frame,
        apply_mask=True,
    ):

    # qr code 이미지에 inner image를 넣는다.
    
    img_inner = Image.open(path_img_inner).convert('RGBA')
    width_img_inner, height_img_inner = img_inner.size

    # resize the inner image if it is too large
    side_longer_img_inner = max(width_img_inner, height_img_inner)
    if side_longer_img_inner > side_img_inner:
        scale = side_img_inner / side_longer_img_inner
        img_inner = img_inner.resize((int(width_img_inner * scale), int(height_img_inner * scale)))
        width_img_inner, height_img_inner = img_inner.size

    if not apply_mask:
        return img_inner
    
    # create a circular mask for the inner image
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

    # apply the circular mask to the inner image
    img_inner = Image.composite(
        img_inner,
        Image.new('RGBA', img_inner.size, (255, 255, 255, 255)),
        mask
    )

    # expand image with white background and padding
    img_inner = ImageOps.expand(img_inner, border=thickness_frame, fill='white')

    return img_inner


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
        'side_img_inner': side_img_inner,
        'thickness_frame': thickness_frame,
        'x_img_inner': x_img_inner,
        'y_img_inner': y_img_inner,
        'path_img_inner': path_img_inner if isinstance(path_img_inner, str) else None,
    }
    return inputs


def set_user_inputs(data):
    global formatted_name, name_prefix, name_family, name_middle, name_given, name_suffix, company
    global type_url_1, url_1, type_url_2, url_2, type_url_3, url_3, type_url_4, url_4
    global type_email_1, email_1, type_email_2, email_2, type_email_3, email_3, type_email_4, email_4
    global tel_mobile, tel_office, note, type_box, size_box, thickness_border_in_box
    global side_img_inner, thickness_frame, x_img_inner, y_img_inner, path_img_inner

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
    side_img_inner = data['side_img_inner']
    thickness_frame = data['thickness_frame']
    x_img_inner = data['x_img_inner']
    y_img_inner = data['y_img_inner']
    path_img_inner = data['path_img_inner']


def process_button_create_qr_code_clicked():

    # qr 코드 이미지를 생성한다.
    img_qr_code = create_img_qr_code(
        type_box=type_box,
        size_box=size_box,
        thickness_border_in_box=thickness_border_in_box,
    )    


    # inner image가 있을 때만 실행한다.
    if use_inner_image and path_img_inner:
        # inner image를 생성한다.
        img_inner = create_img_inner(
            path_img_inner=path_img_inner,
            side_img_inner=side_img_inner,
            thickness_frame=thickness_frame,
            apply_mask=apply_mask,
        )

        # qr 코드 이미지에 inner image를 넣는다.
        x_pos = img_qr_code.width - side_img_inner - thickness_frame - x_img_inner
        y_pos = img_qr_code.height - side_img_inner - thickness_frame - y_img_inner

        img_qr_code.paste(
            img_inner,
            (x_pos, y_pos),
            mask=img_inner.split()[3],
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
        )


if __name__ == '__main__':
    # Initialize path_img_inner and img_inner to None to prevent reference errors
    path_img_inner = None
    img_inner = None
    apply_mask = False

    # default user inputs
    dir_json = Path('json_user_inputs')
    dir_json.mkdir(exist_ok=True)

    # Check if this is the first run
    if 'initialized' not in st.session_state:
        st.session_state.initialized = True
        first_run = True
    else:
        first_run = False

    if 'user_inputs' not in st.session_state:
        user_inputs = load_inputs_from_json(dir_json/'default_user_inputs.json')
        set_user_inputs(user_inputs)
        st.session_state.user_inputs = user_inputs
    else:
        user_inputs = st.session_state.user_inputs
        set_user_inputs(user_inputs)

    st.title(f'QR 코드 명함 생성기 {release_version}')
    st.write('- 스마트폰 카메라로 QR 코드를 스캔하면 연락처 앱에 데이터가 자동으로 입력되는 QR 코드 이미지를 만듭니다.')
    st.write('- 종이 명함 대신 사용되어 환경에 도움이 되면 좋겠습니다.')
    st.write('- 간략 사용법: 명함 데이터를 입력하고 "QR 코드 생성" 버튼을 클릭하세요. 이미지를 다운로드 받으세요.')
    st.write('- 상세 사용법: https://github.com/hsl38/qr_vcard')
    st.divider()


    # 페이지 레이아웃
    col_vcard, col_para, col_qr_code = st.columns([4, 2, 3])

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

        col_download, col_upload = st.columns(2)

        with col_download:
            # Save inputs button
            user_inputs = get_user_inputs()
            json_data = json.dumps(user_inputs, ensure_ascii=False, indent=4)
            st.download_button(
                label='다운로드 입력 데이터',
                data=json_data,
                file_name='user_inputs.json',
                mime='application/json',
            )
    

        with col_upload:
            # user input json을 로드한다.
            json_user_input = st.file_uploader('업로드 입력 데이터', type='json', key='json_user_input')
            if json_user_input is not None:
                user_inputs = json.load(json_user_input)

                set_user_inputs(user_inputs)
                st.session_state.user_inputs = user_inputs
                st.success('QR 코드 생성 버튼을 클릭하면 파일의 데이터가 적용됩니다.')


    # qr code 생성 파라미터 입력
    with col_para:

        # inner image
        use_inner_image = st.checkbox('Inner Image 사용', value=True)

        if use_inner_image:
            path_img_inner = st.file_uploader('QR 코드에 넣을 이미지', type=['png', 'jpg', 'jpeg'], key='inner_img', disabled=(not use_inner_image))

            if path_img_inner:
                # st.text(f'이미지 파일 = {path_img_inner}')    

                st.image(path_img_inner, width=100)
                # st.image(path_img_inner)

                img_inner = Image.open(path_img_inner)

                width_img_inner, height_img_inner = img_inner.size

                st.text(f'이미지 크기 = {width_img_inner} x {height_img_inner}')
        else:
            path_img_inner = None

        if use_inner_image and (img_inner is not None):
            with st.expander('이미지 사용법', expanded=(img_inner is not None)):
                st.write('이미지는 오른쪽 아래에 위치합니다.')
                st.write('마스크를 적용하면 원형으로 잘립니다.')
                st.write('이미지 크기가 너무 크면 QR 코드가 읽히지 않을 수 있습니다.')

        with st.form('qr_code_para'):
            button_create_qr_code_clicked = st.form_submit_button('QR 코드 생성', type='primary', use_container_width=True)

            # qr code 종류
            types_box = ['rounded square', 'vertical', 'standard']
            type_box = st.selectbox('QR 코드 종류', types_box, index=1)

            # qr code 박스(픽셀,  도트) 크기
            size_box = st.number_input('박스 크기', value=4, min_value=1, max_value=8)

            # qr code 테두리 굵기. 박스 크기의 몇 배로 할 것인가.
            thickness_border_in_box = st.number_input('QR 코드 테두리[박스 크기]', value=4, min_value=1, max_value=8)

            # inner image 크기
            # inner image가 있을 때만 입력할 수 있다.
            # 박스 크기의 16배로 하는 것이 기본값이다.
            # 너무 크면 qr 코드 영역이 작아 코드가 읽어지지 않는다.
            # inner image는 오른쪽 아래에 위치한다.
            if path_img_inner:
                side_img_inner = st.number_input('이미지 크기', value=size_box * 16, min_value=32, max_value=128)
                thickness_frame = st.number_input('이미지 테두리', value=2, min_value=0, max_value=8)
        
                x_img_inner = st.number_input('이미지 수평 이동', value=size_box * 6, min_value=0, max_value=640, step=size_box)
                y_img_inner = st.number_input('이미지 수직 이동', value=size_box * 6, min_value=0, max_value=640, step=size_box)

                apply_mask = st.checkbox('이미지 마스크 적용', value=True)
            else:
                side_img_inner = 0
                thickness_frame = 0
                x_img_inner = 0
                y_img_inner = 0
                apply_mask = False


    # qr 코드 생성
    if button_create_qr_code_clicked:
        process_button_create_qr_code_clicked()

    # 자동 QR 코드 생성 (처음 실행할 때만)
    if first_run:
        # Initialize default settings for QR code
        use_inner_image = True
        side_img_inner = 64
        thickness_frame = 2
        x_img_inner = 24
        y_img_inner = 24
        apply_mask = True
        path_img_inner = 'img_inner/cat.png'
        
        # Generate QR code on first run
        process_button_create_qr_code_clicked()

