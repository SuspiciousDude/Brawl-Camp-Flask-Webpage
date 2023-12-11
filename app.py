from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

portrait_maps = {
    'SHELLY': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9FWjFMWW1TWGI2MVM1aFEzd0ZtMi5wbmcifQ:supercell:HUiUs2fa84HT0hJG2xkCqKzhlARqk5mZ1jylVzCCv1U?width=800',
    'COLT': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC80bkNrUzZvcXFqMllOSHZhM2NUNC5wbmcifQ:supercell:gtzUwqunVs0iw7Rih62U3yi5a0bcJxULCLCCgjk4qZ0?width=800',
    'BULL': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC95ZkhEZkZjeVg5RWlvRXpoMThZQS5wbmcifQ:supercell:Guo6ROpxVo_n_teAJM86exa2VKCxRbiOZvb625wqD8M?width=800',
    'BROCK': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC94RDczVjhlR3RSMmdNbTEzdGlFMS5wbmcifQ:supercell:nZv2YI2ZPZ1gI5MuYf0ZFviJNHOR9MTzVR7_FIfAv5g?width=800',
    'RICO': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9ZQXgxODRETWtOZG1mVlFrVVFINC5wbmcifQ:supercell:ohOLINWGkNo8_s6sG5U13ekx0WMU7Z8XFvCJOs-n4ZE?width=800',
    'SPIKE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC8xOHR0UHc3TUYxWlg0YXVNeUdudi5wbmcifQ:supercell:sSsoo5WqAR_hzUTFYjkXvQGVqVwldIMU5e1VadW_LA8?width=800',
    'BARLEY': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9xdjRhNTJGb0Q2eGV2SDNEbVJtOS5wbmcifQ:supercell:LWr6ljGAJ1topr3m92G7kkbHcRDC6qdivlb3P72lK0k?width=800',
    'JESSIE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9jckpyNUtzVHo1ZmoyM1pleWNHOS5wbmcifQ:supercell:B0LaWLp6TLiwSbanYtm2xlcpMiv1YBMNzShzR9c0Hhw?width=800',
    'NITA': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9abU1CUldGaXl5OFBEd3Y4VFFVRS5wbmcifQ:supercell:o2wEbDkz7ofYibHy6KqmBPIZxQ0baLJ1GSrjcYr6NAg?width=800',
    'DYNAMIKE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC80cEpnclIyWmtTeFduRHEzZ1BpWC5wbmcifQ:supercell:RvvbOKhomiGM8aJlMbcXuqzdSKfZYuNZrt2Phi-9mPI?width=800',
    'EL PRIMO': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9xZUJXYlJ3UXNvdkg5Nml0MUp4di5wbmcifQ:supercell:5uKPRVcoGX0f1mevAj9868ntSRDkAGi3Z9i-e3gZrzU?width=800',
    'MORTIS': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9jeWdhZ3NqdUJ5MU51bmVUMVZjRS5wbmcifQ:supercell:_W2KfFdUpO9oetzFH68ThdxFnjywK8s8Qo8gNMTpls0?width=800',
    'CROW': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9xUHRZWlZLaG4zczI2M3NjRVdhRC5wbmcifQ:supercell:br3iLcgqpZBtkgEnm5RWP-DCEubgkNPRnshgYeFp3v0?width=800',
    'POCO': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9XRmNYYmVCTmVMWUtpdzVrZTNkRi5wbmcifQ:supercell:KttSUrrLFcx_kXCp91Gek9HVCrcCX_zoa7ysmOMGahY?width=800',
    'BO': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9YanhuTU43S0xxUGkzQmtxbmM4RS5wbmcifQ:supercell:PALhs_z5LlWmz1udqekaFNWTvzw31l6ia29kVfL5Kl8?width=800',
    'PIPER': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9GUEhqdEpFc2Y3dm5VSDhBeFIxMS5wbmcifQ:supercell:nr3R-KYLiQdResJaiziGul1gOWt2cZOOzNRKsNyL-00?width=800',
    'PAM': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9rSGIxdmduMnhOUldxV3J4RWFFeC5wbmcifQ:supercell:d5PbKaLAEiB85c-XsLDEwwXnk7sIg-_TBK_R9WdM6r8?width=800',
    'TARA': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9GZlFxNW1WcExDWmVrenhIa3hTeC5wbmcifQ:supercell:tQlWT9Tu8vomVCXSaEjn-UakR174QUoZiz35l7BOQ-M?width=800',
    'DARRYL': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9qMU5xNlBpcWRxMWNqQlk3dllBcC5wbmcifQ:supercell:T08nP-hgwpgMDMIon1FRdO2EtbzCHs1SxQZ61WxkYhE?width=800',
    'PENNY': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9wWnpBVVlyYjZiV0FUbXBuTmZHOS5wbmcifQ:supercell:QI8OqvAqT9HWAEZ7KmCWQTlqYaENThw4XKZVIWNymXo?width=800',
    'FRANK': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9WejFnNzFGb0V3MWNZR2ZDdW9MZi5wbmcifQ:supercell:SgBvUNMotrj3L9EU51qlGtnfs_k3-3vDzpUdvvwK7fI?width=800',
    'GENE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9jYXNId1FzRkY5Y0g1UGoxelFNZS5wbmcifQ:supercell:aExv09VhGXQvpUvRJNJ2yDrW48OAdaxceMrMRPdi0ss?width=800',
    'TICK': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9LY2dMV1FpN1htSzdMbWJEUjN2Qi5wbmcifQ:supercell:gqoZwaLMRv-Apf15iKe6lBRTd4naeGRL6nhdwTXeVWI?width=800',
    'LEON': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9HS1RYMnBNQ0M1Q1VOSnRhdXNjUy5wbmcifQ:supercell:swxIDbKMbsfsyaHLthsQWRWthBfu7TAZQddLtmNOdJ8?width=800',
    'ROSA': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9RaThyb2RhNDlpTWNkRG1VNTJHNS5wbmcifQ:supercell:hHiBOBd5e4_08D4vwAcyMSTQdyL_JTYWb2fcndqzI4c?width=800',
    'CARL': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC91NEJ1emNUTThTbTZKY2M0NU0xci5wbmcifQ:supercell:BU_lX9N0RsLIjkecrmp3Ra6C3jCoNc3WkHxnZ-OZfEg?width=800',
    'BIBI': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9Xck4yVHpDWlBDbXI2R0ZhM2lUay5wbmcifQ:supercell:KKPJhz6boSVy47her4AOWsKOninos5SWdCb16X4vbxw?width=800',
    '8-BIT': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9ZTW92NHlTdFlRelo1aTM4d3ZjcC5wbmcifQ:supercell:qqrUTFE3EbvHbAVjZ_sY69EHpFPnnPmy2VNNuLE5omM?width=800',
    'SANDY': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9zY3llZnJCNExSN1dmc2ozemtYVi5wbmcifQ:supercell:a704MYu24gXZv4sEu7PbXgJhblJnJuPe8_EBXRmHlp8?width=800',
    'BEA': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9UOHpRUndmeUdRS3RNTEdDNmdnSi5wbmcifQ:supercell:ZCQ3hDkkxvrpXOgRtmIUN2qmWfP8i97NUuTt45QQEhI?width=800',
    'EMZ': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9CUVlKY1FWOGJjZVI0Z01BbWFYeC5wbmcifQ:supercell:3hyc94swlPO2417Xg5UegRSy5K3lqCa4kz0LlNxV0a8?width=800',
    'MR. P': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC84WlJwSFlRV2p5RnVzZnZZNGo0Wi5wbmcifQ:supercell:LmZPiv7yWSs3A9bHxhMwrTIuRfc72pue-wMOJ4Qscg4?width=800',
    'MAX': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC94cXFwSlkySHdRYWJyUHpHcGMzRS5wbmcifQ:supercell:3xA84_AsOASfu_CrYYaFlLNt5j6-iEyjDw6avvXjlII?width=800',
    'JACKY': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9KN2tqSnFlVVlUQXpBbjlQTmJHdi5wbmcifQ:supercell:BT5nz4UViTtMKC6FGq2U6kJHXxX7Ku-Y8gyQq06qpn0?width=800',
    'GALE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9CQmVIRXp6QzJTZlRIMk1wOXB4cC5wbmcifQ:supercell:0obZShTBtM73Bs-qyIge39JhsaAqOBj-b87HvoNbzik?width=800',
    'NANI': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9rVWo1VzJicHJDQ2IzTFFFVkxrei5wbmcifQ:supercell:o5xVlTidhJazYaR4-Q9DPdoBkY6Atcax-nJvk6BbY98?width=800',
    'SPROUT': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC8yNndoSlFFQ3hqY0xVZWt4WTNhSi5wbmcifQ:supercell:q3ceRm6km7JsyonM7F6dUZBKN7GHvX_31bhFwstVXKo?width=800',
    'SURGE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9vOUs1cHNxYm41blNFaW5CMmdmbS5wbmcifQ:supercell:lX8HgmgfAZbHmteNzjcwQbKdUiSpzn2I7mmdy6IZWdw?width=800',
    'COLETTE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9NNlYyQkpLQTlpejduNHBRenp2WS5wbmcifQ:supercell:GPxSNZgi3qZ5hABKN5ZwshDKl40fmfVM2haeDarg4Q4?width=800',
    'AMBER': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC94a3EyTWRTSmRzdjNrb2tyWkw1TC5wbmcifQ:supercell:oumU4NtFP17aSBIndGVXPtPp3pxemS0qF2_9uD6-UAA?width=800',
    'LOU': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC8xcExCR1dOdkNYdFBHb0piV2luVS5wbmcifQ:supercell:-4rXAxRX7KGjV-ZoIdHb0IP3q7tEJts-SUbTns1nt0Q?width=800',
    'BYRON': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9aQ29qUWdZQXRNUDdyaVJ1RFlkVi5wbmcifQ:supercell:Likm4j3bZHV4LOvKJawmzUzRzHnlXdJwJZsNneWRg0k?width=800',
    'EDGAR': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC85TTVzcHpoTHZzeG95V0Vub1FoZS5wbmcifQ:supercell:An59t9cZklHgOl87teR7xvcKMeya6OOKOuHaeld0Gzk?width=800',
    'RUFFS': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9DVkNGYVBCZTJMZDU3Y29rN0s2Qi5wbmcifQ:supercell:7Ijl3VC1vTvd4Md5Q2s73KoDLBzfVOg_22KWgFwAQZI?width=800',
    'STU': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9DU0FNRHZLeWNIdTNhdG9FWnhFRC5wbmcifQ:supercell:YP0FO_t7CVxPzTJENL_BbAxLoE5E7KvnTHKcev9yAgo?width=800',
    'BELLE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC8xZ0tEQTV3bmpMRXF4OVIybUFNZS5wbmcifQ:supercell:natnrIgo6xwPIN-H29qbdWgaZAMA3sK5jgzmquQe7k0?width=800',
    'SQUEAK': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC8zWEdlU1Z6RjRZVXc5RG5qd1l3ZS5wbmcifQ:supercell:psiN8sCzBR_jwfNqd6T53Fv4XY-oMAlD_OhJg1uhgIU?width=800',
    'GROM': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC85SmNvd3dFV3VwY2hrY1RWWUQycC5wbmcifQ:supercell:RUTwlccFiGEJ3RTvhQJXeQPqA1WbbqXGdCpsFUE2yDg?width=800',
    'BUZZ': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC85WGtjb3JWelNOQmdpdlQ1RGRkNC5wbmcifQ:supercell:gDpGk6LlI6GJ1o8MeryA1Ca8COIuYziB0L8dydSqk18?width=800',
    'GRIFF': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9lZEVtaUxyUlZRZlQyamllM1c1UC5wbmcifQ:supercell:0t1_qe-4l-MtWWtItCdIbIhamAlC5YYbXtSnQ1WIGPU?width=800',
    'ASH': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9UcW5nd1c5Zlgxa21MS0JpaTNBci5wbmcifQ:supercell:NKB4OmhCrJXv1Mg4liuV_AgAsbFdpQ-HVl16swnT-VQ?width=800',
    'MEG': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC8xUVB0V1M3M1dBRW9iYnh3WHV4UC5wbmcifQ:supercell:Wf9PhNr26HouiLvKFVxd5a_21aVQ8DVOAsQ-GTU3Les?width=800',
    'LOLA': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC96WWdSVUx3eDZVdFdMbU53YlR0RS5wbmcifQ:supercell:9FPC5GixCcMCiSBP49X7GegmCsG1DXgvBbYSUsl9piw?width=800',
    'FANG': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9rdXlZWFk2emZvTWM4VU12OG0xTC5wbmcifQ:supercell:ltahdhBIQkyeGufrLQL3JkkQbWn9i6xDXaYDs699iYE?width=800',
    'EVE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9oMTNTOXNXR21zUHB4aXM5SENpYS5wbmcifQ:supercell:sDMByqiRLwPN5dqyjPkkaCncQoH9FYiUZUstFPaJnWo?width=800',
    'JANET': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9iSENFS0FzU3QzbnExZFYxZDFpeC5wbmcifQ:supercell:-qf_u4f0Ag8AvH4UZegHECdJ2TI4xZPHvkKvTkQyBO4?width=800',
    'BONNIE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC8yODNlNVllaUdkTHh2WWZ2UkZGNC5wbmcifQ:supercell:3c2jAGonMKinRbX7enNUqejFRhnKZUtxmDwYqvNXGbM?width=800',
    'OTIS': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9aTlBmTEJ2Mlo1TnMxWlR2RzI4bS5wbmcifQ:supercell:Ova669B6wcpgHk-P3tpXN3JAVnnVLCWr2OH7NNpMI6I?width=800',
    'SAM': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9XTGo5b2lxNXpwS2tmVUJlNHlMdi5wbmcifQ:supercell:EUbbAyRhbOERTZkwyDhI3AASuz2uqkeVQYTab4NDSwc?width=800',
    'GUS': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9ENDlEcG1hMUhqQjk1Vmo5cHFTby5wbmcifQ:supercell:c_b5QZoOX9RvZEt_skbMygDp36V2FNaN4RCiOki9J-I?width=800',
    'BUSTER': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC92cXd1YkJLRHU2RUhndE1lUDJkWC5wbmcifQ:supercell:GR744ml8FYyfzXvNmNQQpBTid50HDm1ZvBQZpbtSF3A?width=800',
    'CHESTER': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9jV3NBdG1udDRMN1EyWHYxQ0NXVC5wbmcifQ:supercell:QREQREg6461JK4UUFcB-ECku18WsP5joWJa7EPFOEaQ?width=800',
    'GRAY': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9mamc2YnFnWEhrMXhKMTVaVW00WC5wbmcifQ:supercell:sYSjJgUoQTgv_Y3Wgw2YKrSbpQc6ANLlDFsaqJftKOY?width=800',
    'MANDY': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9qRmFSZEtaV3NXQU1URDE0amRleS5wbmcifQ:supercell:O5afbsiOOz3AfQjHqe3lTcdgjeXZyRL6QSvkR4Rnec8?width=800',
    'R-T': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC83aHFNRW55WXF0bnJqa3A4WWZ6Yi5wbmcifQ:supercell:PgtsEYzikMp8Kr3EvHt23VqQ8TLnfcyZ5nHWaLkAd9c?width=800',
    'WILLOW': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC95RVNtMUx0VVdaUGozRVhQQmFlNi5wbmcifQ:supercell:H0mljcK2t6JcXtCKLhQMDXxHkN9ntEqLM3Pq9A87zvQ?width=800',
    'MAISIE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9hQkdnb2Y3UDMxcENIZlhUSkU3di5wbmcifQ:supercell:B4AbvSijHaoQEuGGCIJg2dUv2YDgovnrIzPGJoScIrs?width=800',
    'HANK': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC8zeEtWQ0RDc0MxeFQ2UHg5cDhoYy5wbmcifQ:supercell:BIMMCEHGXVKW2VYzLt1sKHBI4nFZCO_7ZIRjjFuIzZo?width=800',
    'CORDELIUS': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9Ya0RlN21Sc3I0RmJwY3RlRndqaS5wbmcifQ:supercell:Rf-4o-SRWHlZEQaEHed8G_jdy73V65Ke2kox4TMHsWU?width=800',
    'DOUG': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC9uclVFUUFHdVo3SHlLeWlhakN5Ny5wbmcifQ:supercell:dbUY6OD8FfK7yZfLSVwBCAHKl67zBqTCFyUJAiWdR5U?width=800',
    'PEARL': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC94YWoyWVRUMjM3RDNQUHRyNFlQeS5wbmcifQ:supercell:r4l5auW4h0mEQ0cK2cKa_6YaLmFFmLcFK8WWwU6TF0w?width=800',
    'CHUCK': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC90eVhTa283Ukt2VGVvSG5HelZQcS5wbmcifQ:supercell:rmc90OlfPNgV2avmYmKq5u89eDEgo0MfGbnxMIi0N10?width=800',
    'CHARLIE': 'https://cdn-assets-eu.frontify.com/s3/frontify-enterprise-files-eu/eyJwYXRoIjoic3VwZXJjZWxsXC9maWxlXC96THQ0VEoxTkdpb3BvWjRxOFRCMS5wbmcifQ:supercell:0_xG5EPkMs3LNUal7B4Bok4H5KLqlxAs7mA9KK2S4sI?width=800'
}

@app.route('/player', methods=['GET', 'POST'])
def player():
    if request.method == 'POST':
        # If the form is submitted, redirect to the same route with the entered player tag
        player_tag = request.form.get('tag')
        return redirect(url_for('player', tag=player_tag))

    # If the form is not submitted, retrieve player data based on the URL parameter
    tag = request.args.get('tag')
    if tag:
        api_key = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6ImZkNWRmMDBkLTFmODktNGU5Mi04ZjhkLWVmYzI1ZGJlMzgxYyIsImlhdCI6MTcwMjI3MTU1Miwic3ViIjoiZGV2ZWxvcGVyL2I4MmRlYTNlLTdlMDktODc2Mi0wNTY2LWI5MDU0NDk1Y2VlMCIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiMTA2LjE5OC4xNjkuMTE1Il0sInR5cGUiOiJjbGllbnQifV19.FHT7xuSfJxTporpReXAE5e4om0tj-bvPYttD033GeGKNV8hQ23g4xwvCPe1p3FBE3EXuy_wAh_O2WsEHpjzDrg'
        api_url = f'https://api.brawlstars.com/v1/players/%23{tag}'
        headers = {'Authorization': f'Bearer {api_key}'}

        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            player_data = response.json()
        else:
            player_data = None
    else:
        player_data = None

    if player_data and 'brawlers' in player_data:
        for brawler in player_data['brawlers']:
            brawler_name = brawler['name']
            brawler['icon_url'] = portrait_maps.get(brawler_name)

    return render_template('player.html', player_data=player_data)

if __name__ == '__main__':
    app.run(debug=True)
