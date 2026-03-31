import numpy as np
import pandas as pd
import streamlit as st


INTERVAL = 20

block = np.ones((30,200,3), dtype=np.int16)
df = pd.read_parquet('data/data.parquet')
df = df.astype({
    'r': 'int16',
    'g': 'int16',
    'b': 'int16'
    })

st.markdown('# Stitches Crossed')
st.divider()


col1, col2 = st.columns(2)

with col1:
    input_code = st.text_input(label='DMC Thread Code', value=None)

    if input_code is not None:
        try:
            color = df[df['code'] == input_code].reset_index().loc[0]
            rgb = [
                color['r'],
                color['g'],
                color['b']
            ]
            color_block = block.copy()
            color_block[:,:] = rgb

            # st.markdown(
            #     f'RGB: {rgb[0]}, {rgb[1]}, {rgb[2]}',
            #     text_alignment='center'
            # )
            #
            st.image(color_block, width='stretch')


        except KeyError:
            st.markdown('Code not found!')

with col2:
    if input_code is not None:
        try:
            rlower = rgb[0] - INTERVAL
            rupper = rgb[0] + INTERVAL
            glower = rgb[1] - INTERVAL
            gupper = rgb[1] + INTERVAL
            blower = rgb[2] - INTERVAL
            bupper = rgb[2] + INTERVAL

            mask = (
                (df['code'] != input_code) & 
                (df['r'] > rlower) & 
                (df['r'] < rupper) & 
                (df['g'] > glower) & 
                (df['g'] < gupper) & 
                (df['b']> blower) & 
                (df['b'] < bupper)
            )

            df_analogues = df[mask].copy().reset_index()

            if df_analogues.shape[0] != 0:
                length = df_analogues.shape[0]

                for row in range(0, length):
                    temp = df_analogues.loc[row]
                    code_analogue = temp['code']
                    rgb_analogue = [
                        temp['r'],
                        temp['g'],
                        temp['b']
                    ]

                    analogue_block = block.copy()
                    analogue_block[:,:] = rgb_analogue

                    st.markdown(f'Code: {code_analogue}')
                    # st.markdown(
                    #     f'RGB: {rgb_analogue[0]}, {rgb_analogue[1]}, {rgb_analogue[2]}',
                    #     text_alignment='center'
                    # )
                    st.image(analogue_block, width='stretch')
                    st.markdown(' ')
        except NameError:
            st.markdown('Code not found.')
