#!/usr/bin/env python3
from __future__ import annotations

import base64
import json
import os
import socket
import re
import tempfile
import subprocess
import zlib
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

PLAYER = Path.home() / ".cache/solace-player/solace-pro-ble-direct-engine.py"
APP_VERSION = "v1.2.3-Visible-FR-EN"
APP_NAME = f"Solace Funscript Player {APP_VERSION}"
PYTHON = Path.home() / "buttplug-player-venv/bin/python"
CONFIG = Path.home() / ".config/solace-player-gui.json"
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v"}
VIDEO_TYPES = (
    ("Vidéos", "*.mp4 *.mkv *.avi *.mov *.webm *.m4v"),
    ("Tous les fichiers", "*"),
)

COLORS = {
    "bg": "#050810",
    "panel": "#0A1020",
    "panel_alt": "#0F1830",
    "border": "#173A5E",
    "text": "#EAF8FF",
    "muted": "#78A0B8",
    "accent": "#00CFFF",
    "accent_hover": "#59E6FF",
    "success": "#35F2A1",
    "warning": "#FFC857",
    "danger": "#FF4D7D",
    "track": "#14243B",
}

ENGINE_BUNDLE = 'c-pO7&2rp0lD^kdVA!$IEO(Krk}OA0ZC6LQJ@SlZ{G+hE-i=Tz7^osj;+REp2vR?xQAc0*y!!xq+E~Xt!raDh(oeFP_#pujq~zY!!LA}R6NyCrd`O_a`psU=%e{4y?Xm2N6t~r7o*hiKWxgX(w5_YUWKl$tU6Gd+p;?w!v`X@fPbT_Vc~Q`kv*tU$%{ED{zpfL`HkJPNXP#&JbI$cAo?K)!ZNBB3kF4R~^|~nY4dX5KZS%2WyJDN9&Dd44V^a5mR+nkA){39NSNWp4Et2d)KYyOxP9{}(yPOdC69ns&(U1E55BTLpny{>z$uFlHFaj$l>}JD?iX02Nqq59PDWfQptn$T2{PSMtah)=9A`DCZ@i!&^AAcuw%|UGVW9GHg#~H6^nz8^`Vw!RC)84wSsv@l~f+D52tPHMjo#++Ykfp^+2580F7D+)8DVqdAU0jqjW>OVz*2q9puE4w@uVPk~^2JpATT)m@a(c_b<VQD2<?l}?lhe1ap1(MXPLJMwIDT<NR>XU{|8y~*&lkabzJCxrUB^#@^*TNb=(FGM&)L(>;j_a7PxJljyW{sJ*Zw%yi{~%?faJKA;bp#K{*>$yFWltWHo4g2c}h1d0A~qcUcrWLE?J2F=1nG(O-eZ@uZyeWlNWNGVzvbbPqL(nBA>H#J5!Dqq3bNgC{q%APu}DiTQ(*_%FrMLeT;8?vZZ>hc*tLcJmA9rZ1Q!z-Lev1tv%0vQ?kF*j8{<-!`t~pycA(3W&!ihAjH%pFa+|tT9R#=(+cPp^KkB(NJUG0jr8Fzhq%tOWaCd8g6m80hTdxuD9-Piks1#COSU}|h3qEb75Aq$rBDK>8Vf2OUwwQ2GWwS{$N#36B|Lrm;!n}(`*%mrUr(KaLe8pn3LhZ8{g*W5tWVd3diRfB)1=8=;RUE()>#IUqBPG7e=3xVw5gpUv>u>wRr*~kOr1RLrwy;NjgzQkkejpKE0veto*FsHX{}9~bLQI$*jC^vV}%dybJ$YJJn&vFy%@sxFb8s;tTAUXP+of^I5Vx)@{!jkA3|^1^If3?&e!3hrZ16%6L7)~g=H+~j7(FCkn07{Zb!3N1&{i+Bq@0885D<ep%#1?)~c_Ow9yM`1gMqDOke>5>4!j&?>>KOjNyv%Zy;=2lbg}sp=^i>dJFN66qxeDxZV}qcGEjg&CXludCrK}ih{@Om-|`AicsQdm6v?wdovICmfo}_nT9Oe<S{1XZy<YNS(<!VU_m8}p*FQqGt)CNtRyqi`?BuXTRs=#3Li-_GokiFAf^=sLp@Hjl5MU`wVoXw9z5%ZEqDbEjiTK#H{ujjxdee(sAT6kQk+pEz&~&#izZDnHtSRp<6Fp!6w0=+(u^!@`6c58U^=GV2My1Clo-ZLuI#j%<~0vm&NuyNN>(ewm6k4B*~|=W0ers!EWqmxf<14{itp+Si;pxRCR?YtY2Su2XLd$MOZGDp`U7Bzf|b>+$_^Rbu_Y$=eo|0^rArB`>%?;AnUXvy<$T&;l2>44TE46^zA2NU8U!Z~qY^6oimT*R)kVtA62z_W&-pnl?b*4_fHu_RNaG-h&=Y)Fzgo@2!$+u9(rb_@FhI#@998V5@<pnEC|h}TwGF-v0Q`FpYZc7i$lcQIO6`z;JbnA-ck+=zl*Bgz5H(EsrrrUj=Jrfven8^yAjC2s)S9|7h)n^Tofv0u29M9fg!2O6r3=I$o0YJYkK^<2R|6yB-x`c!*Y<q<=NW-i2>L4nguoi97=({Alxq8RGwF~P1@QVHq!X;dOz_I67O-K9Z7Xf_Qf5X-pN-5OxD)x6i>*Wk=0JuSiIYv`m><A^D#>bQy})6lr;34qUq+$wUI>u0bBC;9;D#U;w_H-dnMW({+zqP$r2y@Y-uUww*(I3|n~s^q3lzZYNE`}P`F~=!BJ0e^``d!4j~{4S%g<A{j!r`;gM$9xBy%^TTqnJ-K80Wg6%G9q0f#-PZ&b=UOCbIB*EfOP8=76R^%hsLq2tSsXTjq9Y<`Xj9a-UHU(c43NGgkh0Sq7F(epwkLwQgHV@A?UAtLu(@TxVs@4aGVs}m^rE~H?zILi_NKzBK~E5uWMqa2U-v6p%QGmyhN5+z#m291G+yg@5U((^Vk!rCM#C!%^cwuAf%4kmJ=*pOK`a>vPcD@y^8-!rnRErQ+e5-$v2mlD74NR&(XSdmDLGCMg|c5y=aUsNU+mx@oA2ItwTQ9)1@bJ9@*<pgBW`eU^KvW0`}+?-IgKoeE-5&esWp>B!YDG=&|B?92X7J(!KN#a4bW`nBV5D)@y3m|_YML>P-?XV-+V(|HfW`J1XY0T9=TP(2AERyPq9z-0`I0nSQ%}u|0gIK_PY-KqGQw=~SIv~TP)H4!8Z)hXa%4c4WSZUKz;sZsd65x^e4_0bvq#(|v{b9N6VV73&p%u341UxTkcENmbfTx{|=}hyTmYP*fJb|chu$;t6iJMLg`BSk_1Tgh3FB1;X`p(wuo_GWDe);)738W6}a$YfVr<A_mJNV`2|L*hjE5$~vKbX<*2HzgM&m?i9WDRwbLG@Qwi}`fGBwJ5SRI$K3uM#R3f%tdkvV#4;&T>rtNLzn>KXvUfR7glgCXNEwtUn-Se6}3a?DN0F;2WjOlH39Dy*D&-yW_A34^>1z#%&zlvGv|D7`DWre|UAI++pw4hf{(Dhr;^YSwVbpPk6^89_tAvWW7o@qE5(3neE~*PWUFj0`#g^)g0f*U+^?eAOdB*v4Nh1XaY9Lp}O@u4#iqy{qBd0d>PhIb4%RZVi%8JC)Fj?&kv`8V{KqGPqu13F{mYA;tqpztB$v`u^mOOnfD4Tg1gT6^QTI<FDJ{69?g`8M43KEAcx;cHSY<2($Q|#d;I%~0Ax_Hb5iCF-h}|-U*jPMU|WJ#`C+jiTAZyK5_I)+`N(cpDc!AOO5!DPXRSHf##gI_R)!6bGAlwYPmSye^h6djrx25U_CR9l>=?kc+Iavtn7E92^7#|ssZ0D9K_Mj3RCX>hu+nnS&JX6ohT7G797%zl1^j@DZ4*XNxfGLLNzsKM-B&_k4aPE-!rqSYij<!};b&ZEm?d}{d|;jBy#!<o3g7kHFIDMp!n#i4DOBU@UI=Js<*dZm6fP?#qn>al`9^lD1VxCWQ|z1K95yz?eK*+6Llmu%ZhwhsEXT`?$Vk%6jzZAyvkcVB#t$-Ka{l>$VuqN&xh6))4b|T}b6)qMtK?dbBqo9l4bExz5kP=1zwi}y3Sm2qrw>v7QGA^`c&|&?fJi{q8_Z~?-Zj8!Ng5xX5ebr(Dje@|KN-X5tNm#|D7$!VHWH+EDV~hiOC26#%jOxzhX^n8`iibo7Lu2&ggkN#JX=vERZ@P(c6kN%GmaQ(nnIeyHl-np$-v^ACQL2Y)I!hL+l?sSB#AF)v$T&@o2I+&thG%f%VFg@T|ga<(7)T6nI6-cREgECX-{ZicCB?6a3#))W<#3mJmOZq+49Y!#eCjw_S!jUih<UHEkO4kbR)52xfuk=%TrdJf+d!Bn)UvlvA#`E<CNCf<}%t9SN>HJvs||397mfN7gb3kT3+ZDAedhsceF?D;YkjFNo{7NJuO(`!9a!=dqI%p0pu^3Ax-TUknA=rxQ6J+uUEH>+iyRD9|t(rD$C6SX?T@nMO_6+u?a9uvT}82Oy=Goe$vipHZjw-u!LH8S?g4AbtmepIoe);XX$=ksOGA^?hw9#a2Gv6VY5W<`NUxAlv;CzQiG7)6d=9k0)T=0<>{3^uaeCReWYwLH?5690TZJ+Cx!|W9^qlW-^0mU??VD`%Sr)Q%>^4+vwH`iw_RSCgBe<n4cT<JyQ3QXj~lzcOKuxKt8OpdH^jSlvAtc4));apt4l+;-oZRt$p-s0n|p|rNV%K&7(Cnjno*EK(@1uKMQV~{fK|$}E-KNt)dk?_3L%y906exb-t|wk+D?@|p5YZfcO1R8qv5f-Z|ui-a)A)TmzQ?J)8pSCzj;3+?br85?_L{D(A(0ZE?7S!$r4?HOQ+z`@O5S>)|ytW+nc;P-W3wTvDk6I-S#4^QPp<iHPiw1WNB6~+#<^60l__=u7u>x+c%`Hk`x;V2D0sYb<dTj<Ga(7lwL5c$eoUJNSaNtd4k0xoNw=c`T0M(`_h(y-t-yBKbd>eNe_yvl4^Ifw8Vi;DMY)b0B?<C{_UK?TUTPN{MEA932ZXlBgSoMbGb`o+W0-gn^v^EeThlNu?1w?<Yt8hDNr|o<dOyuvb^4km*NN)zQ-(O6%&BaMqro^s$Jo}sM47p&<V(A*s160<}H{yOOx!Q-*al54><PAyw1j5x}QV3)!wS}vu4eZ3CfnyC>AM4-iGp>cT}X80A1Mb5!yyaEn1{mq-&jZmno$fzTj-=n*tCGTzb-kafE0U5Awpf{j#7nXV%3Hx%WFsYfdgoiAGe-W*iDNJl+Brg%pzE4xIop28y4a&dH94U1S)EBzHwqh0H9ogD#72ZG4WfZ5}T60l2|ikhv!TUATYP+L{-P#nG-#tE7OCE2ri)iOB<LK_f*>3mWE;IivuM7Fk(<ZwnfIrZnsIt@N~@#Qt>Goh#-El_+-H)y2}S8CdhW6s?&ZEfL`3MaAA_47uNIYXyJ+Q7(E%ONQfyFozV1&ftxn_H6VKy<v0_bc1!Cr+(|U*73b3s65BH9(rCR&jp8gktD!_!Oq50_uTAYa9#+~e^+>BH8PZz<+;x<VKgaW)N+GSDvv>g1jkec4_IN;QQNY78^B^=s~Idjtd9+BdbxM}kfE0mzl`lyIH3E0e&mwe!F2clyc-RT+YP$Qz##jN9b{)5bqly6&%o5Uc+7=~0Pkz*%$0Aq5W3NhPkZWW60qL|c0B~p|AI66q6-NuL2hS<@``syLWBa5EZ}|-$`7Em7XpDd$U558aW!`aiNpp~+s#{&jv;5`j7>yq#!gfMp2q9B4@i+o4rGWxl;1{p?nmB@x1h$arJ`L+RtUscOn=qQQya}F_i~(7^pdI$)PA5qI_Wz1_saD{aQ=>{0PKCxIZ$&XEl0AlXtMm;b$7ZuGr3fK@n5y&9UIei#u^xdS7@7-QITg*hD8J0B?Mcph<R9cmEW?`WaSd{R^;=40hUTQAa3m2VN0(Tw<2I6a~}4DTDZ%Zr2nt!4=*&yireh2L-XPUBp^Umkev)PC^8z}7QxkU?Ux`UXt_@u{^Z&*fh)KqjkIJd0MV=(=;M`$-+iUz6RH0c+j;he;4-h%SfF0Kq~JEc2G6=WxDMv%n)^zhz~&O}@0uBQO|uK9G#~vr=pb@i5Lk{wvd%V60fyUv(*2E9FEUI+i1W%p4Y~++s8+g~wKKJ5(+3Q_Qgnl4%^n5Rbi%-<)5pqn&Ij<s$VCPT-G40aI=O85+wfqEr_+BOI5ClojZ@#ri7XG|`v+KfUY8q2?o`}}2Et*u5FLcE`Vp_Zk@s83N0;*CWuUT52GdR3?0O*A%)fOvC!EHYMmMhr$v)k_IE6J6J^JC$hDIL6s^8u`x{df_rW%P~+&<i52R*fac7WUVLCop|U&c1x@!N=pakE{nZ4_;)B24E-*pJlIWL5_V)&GOOs_pe<R%`fh_4RLA;<4WiJ#?h{rJAcvxY46r$}Z*SPt8@IusQTu*9oLjaVk;DW^Qvx@w~hc7aLB*OLZV6KI1mjO{H{~WTH_^)qCF)Aj%sdXlnWxQ4nCGF;I<02#V^qU@MXNusOG-by}^Sh4WDn=wiXH;TAXDHShj7tK8}gF^}_tX9hak4ro4qKy#?24~bYjAVRd6g0{`{E5(?T2_!slnq=|dd=xeqw8#T1qB1wI%Zs2Zk5_pK8#pK=<DP^KU-)it%3H-=JNnuAs04AeD4L+-Bk4_RfGJ#&>N})@Lxtmx0xq-<1yzB<HkB2tq4*$<ELGGQ)y%@T9Vn)s_s%$)9wKljI|`5=I2$RzDjtT9C`9|_1a%26>&!RLLlNIj68y0Ww!))GTwjVJG(i-p-|+N)IxGz|o%}B=bG9@'


def ensure_internal_engine() -> None:
    PLAYER.parent.mkdir(parents=True, exist_ok=True)
    engine_data = zlib.decompress(base64.b85decode(ENGINE_BUNDLE.encode("ascii")))
    try:
        current = PLAYER.read_bytes()
    except OSError:
        current = b""
    if current != engine_data:
        PLAYER.write_bytes(engine_data)
        PLAYER.chmod(0o755)


def natural_key(path: Path):
    return [
        int(part) if part.isdigit() else part.casefold()
        for part in re.split(r"(\d+)", path.name)
    ]


def find_script(video: Path) -> Path | None:
    candidates = [
        video.with_suffix(".funscript"),
        video.parent / "Funscript" / f"{video.stem}.funscript",
        video.parent / "funscript" / f"{video.stem}.funscript",
    ]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    return None


def script_candidates_for_deletion(
    video: Path,
    selected_script: Path | None,
) -> list[Path]:
    candidates = [
        video.with_suffix(".funscript"),
        video.parent / "Funscript" / f"{video.stem}.funscript",
        video.parent / "funscript" / f"{video.stem}.funscript",
    ]
    if selected_script is not None:
        candidates.insert(0, selected_script)
    return candidates


class SolacePlayerGUI(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title(APP_NAME)
        self.geometry("1180x780")
        self.minsize(900, 620)
        self.configure(bg=COLORS["bg"])

        try:
            self.attributes("-zoomed", True)
        except tk.TclError:
            pass

        self.video_path = tk.StringVar()
        self.script_path = tk.StringVar(value="Aucun funscript sélectionné")
        self.status = tk.StringVar(value="Choisis une vidéo pour commencer.")
        self.min_position = tk.DoubleVar(value=0.0)
        self.max_position = tk.DoubleVar(value=1.0)
        self.speed_multiplier = tk.DoubleVar(value=1.0)
        self.amplification = tk.DoubleVar(value=0.0)
        self.fullscreen = tk.BooleanVar(value=False)
        self.delete_after_natural_end_var = tk.BooleanVar(value=False)
        self.play_next_var = tk.BooleanVar(value=True)
        self.resume_video_var = tk.BooleanVar(value=True)
        self.language = tk.StringVar(value="fr")

        self.process: subprocess.Popen | None = None
        self.playlist: list[Path] = []
        self.playlist_active = False
        self.delete_after_natural_end = False
        self.stop_requested = False
        self.manual_next_requested = False
        self.current_video: Path | None = None
        self.current_script: Path | None = None
        self.playlist_folder: Path | None = None
        self.last_folder = str(Path.cwd())
        self.resume_positions: dict[str, int] = {}
        self.saved_video_on_startup: Path | None = None
        self.last_position_save_time = 0.0
        self.graph_actions: list[tuple[int, int]] = []
        self.graph_duration_ms = 0
        self.graph_position_ms = 0
        self.progress_file = Path(tempfile.gettempdir()) / f"solace-player-progress-{os.getpid()}.json"
        self.mpv_socket = Path(tempfile.gettempdir()) / f"solace-player-mpv-{os.getpid()}.sock"

        self.configure_styles()
        self.load_config()
        ensure_internal_engine()
        self.build_ui()
        self._restore_last_video()
        self.after(150, self.update_graph_position)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    TEXTS = {
        "fr": {
            "menu_language": "Langue", "french": "Français", "english": "Anglais",
            "timeline": "◈  CHRONOLOGIE FUNSCRIPT  //  CONTRÔLE DE POSITION",
            "back10": "−10 s", "pause": "Pause / Reprendre", "forward10": "+10 s",
            "title": "SOLACE // CENTRE DE CONTRÔLE",
            "subtitle": "BLE DIRECT  •  SYNCHRO MPV  •  FUNSCRIPT LOCAL  •  SANS INTIFACE",
            "media": "01 // SOURCE MÉDIA", "video": "Vidéo", "video_btn": "VIDÉO",
            "folder": "DOSSIER", "script": "Funscript",
            "motion": "02 // MATRICE DE MOUVEMENT",
            "minpos": "Position minimale", "maxpos": "Position maximale",
            "ble": "Réactivité BLE", "amp": "Amplification adaptateur",
            "fullscreen": "Ouvrir MPV en plein écran sur l’écran de droite",
            "delete": "Supprimer la vidéo et son funscript à la fin ou en passant à la suivante",
            "autonext": "Passer automatiquement à la vidéo suivante",
            "resume": "Reprendre la vidéo là où elle a été arrêtée",
            "engage": "▶  LANCER", "folder_play": "▶▶  DOSSIER",
            "next": "⏩  SUIVANTE", "abort": "■  ARRÊTER",
            "no_graph": "Choisis une vidéo avec son funscript",
            "no_script": "Aucun funscript sélectionné",
            "choose_start": "Choisis une vidéo pour commencer.",
        },
        "en": {
            "menu_language": "Language", "french": "French", "english": "English",
            "timeline": "◈  FUNSCRIPT TIMELINE  //  SEEK CONTROL",
            "back10": "−10 s", "pause": "Pause / Resume", "forward10": "+10 s",
            "title": "SOLACE // CONTROL CORE",
            "subtitle": "DIRECT BLE  •  MPV SYNC  •  LOCAL FUNSCRIPT  •  NO INTIFACE",
            "media": "01 // MEDIA SOURCE", "video": "Video", "video_btn": "VIDEO",
            "folder": "FOLDER", "script": "Funscript",
            "motion": "02 // MOTION MATRIX",
            "minpos": "Minimum position", "maxpos": "Maximum position",
            "ble": "BLE responsiveness", "amp": "Adapter amplification",
            "fullscreen": "Open MPV fullscreen on the right display",
            "delete": "Delete video and funscript after completion or when skipping",
            "autonext": "Automatically play the next video",
            "resume": "Resume video from the last saved position",
            "engage": "▶  ENGAGE", "folder_play": "▶▶  FOLDER",
            "next": "⏩  NEXT", "abort": "■  ABORT",
            "no_graph": "Choose a video with its funscript",
            "no_script": "No funscript selected",
            "choose_start": "Choose a video to begin.",
        },
    }

    def tr(self, key: str) -> str:
        return self.TEXTS.get(self.language.get(), self.TEXTS["fr"]).get(key, key)

    def _refresh_language_buttons(self) -> None:
        active = self.language.get()
        for code, button in (
            ("fr", getattr(self, "fr_button", None)),
            ("en", getattr(self, "en_button", None)),
        ):
            if button is None:
                continue
            selected = code == active
            button.configure(
                bg=COLORS["accent"] if selected else COLORS["panel_alt"],
                fg="#001018" if selected else COLORS["text"],
                activebackground=COLORS["accent_hover"],
                activeforeground="#001018",
                highlightbackground=COLORS["accent"] if selected else COLORS["border"],
                highlightthickness=1,
            )

    def set_language(self, language: str) -> None:
        if language not in ("fr", "en"):
            return
        if language == self.language.get():
            self._refresh_language_buttons()
            return
        self.language.set(language)
        self.save_config()
        self.build_ui()
        if self.current_video or self.video_path.get().strip():
            video = self.current_video or Path(self.video_path.get().strip())
            if video.is_file():
                self._set_selected_video(video, announce=False)

    def configure_styles(self) -> None:
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(
            ".",
            background=COLORS["bg"],
            foreground=COLORS["text"],
            bordercolor=COLORS["border"],
            font=("Noto Sans", 10),
        )
        style.configure("Root.TFrame", background=COLORS["bg"])
        style.configure(
            "Card.TFrame",
            background=COLORS["panel"],
            borderwidth=1,
            relief="solid",
        )
        style.configure(
            "Header.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["text"],
            font=("Noto Sans", 24, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["muted"],
        )
        style.configure(
            "CardTitle.TLabel",
            background=COLORS["panel"],
            foreground=COLORS["accent"],
            font=("DejaVu Sans Mono", 11, "bold"),
        )
        style.configure(
            "CardText.TLabel",
            background=COLORS["panel"],
            foreground=COLORS["muted"],
        )
        style.configure(
            "Value.TLabel",
            background=COLORS["panel"],
            foreground=COLORS["accent_hover"],
            font=("DejaVu Sans Mono", 10, "bold"),
        )
        style.configure(
            "Status.TLabel",
            background=COLORS["panel_alt"],
            foreground=COLORS["muted"],
            padding=(12, 9),
        )
        style.configure(
            "Dark.TEntry",
            fieldbackground=COLORS["panel_alt"],
            foreground=COLORS["text"],
            padding=9,
        )
        style.configure(
            "Accent.TButton",
            background=COLORS["accent"],
            foreground="white",
            borderwidth=0,
            padding=(16, 11),
            font=("DejaVu Sans Mono", 10, "bold"),
        )
        style.map(
            "Accent.TButton",
            background=[("active", COLORS["accent_hover"])],
        )
        style.configure(
            "Secondary.TButton",
            background=COLORS["panel_alt"],
            foreground=COLORS["text"],
            padding=(14, 10),
        )
        style.configure(
            "Danger.TButton",
            background="#382028",
            foreground="#ff8797",
            borderwidth=0,
            padding=(14, 10),
            font=("Noto Sans", 10, "bold"),
        )
        style.configure(
            "Dark.Horizontal.TScale",
            background=COLORS["panel"],
            troughcolor=COLORS["track"],
        )
        style.configure(
            "Dark.TCheckbutton",
            background=COLORS["panel"],
            foreground=COLORS["text"],
            padding=4,
        )

    def build_ui(self) -> None:
        for child in self.winfo_children():
            child.destroy()

        self.config(menu="")

        shell = ttk.Frame(self, style="Root.TFrame")
        shell.pack(fill="both", expand=True)

        graph_frame = tk.Frame(
            shell, bg="#02050B", height=165,
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        graph_frame.pack(side="bottom", fill="x")
        graph_frame.pack_propagate(False)

        graph_header = tk.Frame(graph_frame, bg="#050A13", height=34)
        graph_header.pack(side="top", fill="x")
        graph_header.pack_propagate(False)

        tk.Label(
            graph_header,
            text=self.tr("timeline"),
            bg="#050A13", fg=COLORS["accent"],
            font=("Noto Sans", 8, "bold"), padx=10, anchor="w",
        ).pack(side="left", fill="x", expand=True)

        for label, command in (
            (self.tr("back10"), lambda: self.seek_relative(-10)),
            (self.tr("pause"), self.toggle_pause),
            (self.tr("forward10"), lambda: self.seek_relative(10)),
        ):
            tk.Button(
                graph_header, text=label, command=command,
                bg=COLORS["panel_alt"], fg=COLORS["text"],
                activebackground=COLORS["accent"], activeforeground="white",
                relief="flat", bd=0, padx=12, pady=3, cursor="hand2",
            ).pack(side="left", padx=2, pady=3)

        self.graph_canvas = tk.Canvas(
            graph_frame, bg="#020711", highlightthickness=0,
            borderwidth=0, height=110, cursor="hand2",
        )
        self.graph_canvas.pack(side="bottom", fill="both", expand=True)
        self.graph_canvas.bind("<Configure>", lambda _e: self.draw_funscript_graph())
        self.graph_canvas.bind("<Button-1>", self.seek_from_graph)
        self.graph_canvas.bind("<B1-Motion>", self.seek_from_graph)
        self.graph_canvas.bind("<Button-3>", self.toggle_pause)
        self.graph_canvas.bind("<MouseWheel>", self.graph_mousewheel)
        self.graph_canvas.bind("<Button-4>", self.graph_mousewheel)
        self.graph_canvas.bind("<Button-5>", self.graph_mousewheel)

        content = tk.Canvas(
            shell, bg=COLORS["bg"], highlightthickness=0, borderwidth=0,
        )
        scrollbar = ttk.Scrollbar(shell, orient="vertical", command=content.yview)
        content.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        content.pack(side="top", fill="both", expand=True)

        root = ttk.Frame(content, style="Root.TFrame", padding=24)
        window_id = content.create_window((0, 0), window=root, anchor="nw")
        root.columnconfigure(0, weight=1)
        root.bind("<Configure>", lambda _e: content.configure(scrollregion=content.bbox("all")))
        content.bind("<Configure>", lambda e: content.itemconfigure(window_id, width=e.width))

        header = ttk.Frame(root, style="Root.TFrame")
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)
        ttk.Label(header, text=self.tr("title"), style="Header.TLabel").grid(
            row=0, column=0, sticky="w"
        )

        lang_box = tk.Frame(
            header, bg=COLORS["panel"],
            highlightbackground=COLORS["accent"],
            highlightthickness=1,
        )
        lang_box.grid(row=0, column=1, sticky="e", padx=(16, 14))

        tk.Label(
            lang_box, text="LANGUE / LANGUAGE",
            bg=COLORS["panel"], fg=COLORS["accent"],
            font=("DejaVu Sans Mono", 9, "bold"),
            padx=10, pady=6,
        ).pack(side="left")

        self.fr_button = tk.Button(
            lang_box, text="FR", width=5,
            command=lambda: self.set_language("fr"),
            relief="flat", bd=0, cursor="hand2",
            font=("DejaVu Sans Mono", 10, "bold"),
            padx=5, pady=5,
        )
        self.fr_button.pack(side="left", padx=(2, 2), pady=4)

        self.en_button = tk.Button(
            lang_box, text="EN", width=5,
            command=lambda: self.set_language("en"),
            relief="flat", bd=0, cursor="hand2",
            font=("DejaVu Sans Mono", 10, "bold"),
            padx=5, pady=5,
        )
        self.en_button.pack(side="left", padx=(2, 4), pady=4)
        self._refresh_language_buttons()

        ttk.Label(
            header, text=APP_VERSION, style="Subtitle.TLabel"
        ).grid(row=0, column=2, sticky="e")
        ttk.Label(
            root, text=self.tr("subtitle"),
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 18))

        file_card = ttk.Frame(root, style="Card.TFrame", padding=18)
        file_card.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        file_card.columnconfigure(1, weight=1)
        ttk.Label(file_card, text=self.tr("media"), style="CardTitle.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))
        ttk.Label(file_card, text=self.tr("video"), style="CardText.TLabel").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(file_card, textvariable=self.video_path, state="readonly", style="Dark.TEntry").grid(row=1, column=1, sticky="ew", padx=10, pady=6)
        ttk.Button(file_card, text=self.tr("video_btn"), style="Secondary.TButton", command=self.choose_video).grid(row=1, column=2, padx=(0, 6), pady=6)
        ttk.Button(file_card, text=self.tr("folder"), style="Secondary.TButton", command=self.choose_folder).grid(row=1, column=3, pady=6)
        ttk.Label(file_card, text=self.tr("script"), style="CardText.TLabel").grid(row=2, column=0, sticky="nw", pady=6)
        self.script_label = ttk.Label(file_card, textvariable=self.script_path, style="CardText.TLabel", wraplength=760)
        self.script_label.grid(row=2, column=1, columnspan=3, sticky="w", padx=10, pady=6)

        settings = ttk.Frame(root, style="Card.TFrame", padding=18)
        settings.grid(row=3, column=0, sticky="ew", pady=(0, 14))
        settings.columnconfigure(1, weight=1)
        ttk.Label(settings, text=self.tr("motion"), style="CardTitle.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))
        self.add_scale(settings, 1, self.tr("minpos"), self.min_position, 0.0, 0.90, lambda value: f"{float(value) * 100:.0f} %")
        self.add_scale(settings, 2, self.tr("maxpos"), self.max_position, 0.10, 1.0, lambda value: f"{float(value) * 100:.0f} %")
        self.add_scale(settings, 3, self.tr("ble"), self.speed_multiplier, 0.25, 2.0, lambda value: f"{float(value):.2f} ×")
        self.add_scale(
            settings,
            4,
            self.tr("amp"),
            self.amplification,
            0,
            100,
            lambda value: (
                f"{float(value):.0f} %  "
                f"(x{1.0 + 2.0 * float(value) / 100.0:.2f})"
            ),
        )
        ttk.Checkbutton(
            settings, text=self.tr("fullscreen"),
            variable=self.fullscreen, style="Dark.TCheckbutton",
        ).grid(row=5, column=1, sticky="w", padx=10, pady=(10, 2))

        ttk.Checkbutton(
            settings,
            text=self.tr("delete"),
            variable=self.delete_after_natural_end_var,
            style="Dark.TCheckbutton",
        ).grid(row=6, column=1, sticky="w", padx=10, pady=(6, 2))

        ttk.Checkbutton(
            settings,
            text=self.tr("autonext"),
            variable=self.play_next_var,
            style="Dark.TCheckbutton",
        ).grid(row=7, column=1, sticky="w", padx=10, pady=(6, 2))
        ttk.Checkbutton(
            settings,
            text=self.tr("resume"),
            variable=self.resume_video_var,
            style="Dark.TCheckbutton",
        ).grid(row=8, column=1, sticky="w", padx=10, pady=(6, 2))

        actions = ttk.Frame(root, style="Root.TFrame")
        actions.grid(row=4, column=0, sticky="ew", pady=(0, 14))
        actions.columnconfigure(0, weight=1)
        self.launch_button = ttk.Button(actions, text=self.tr("engage"), command=self.launch, state="disabled", style="Accent.TButton")
        self.launch_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.folder_button = ttk.Button(actions, text=self.tr("folder_play"), command=self.launch_folder_playlist, state="disabled", style="Secondary.TButton")
        self.folder_button.grid(row=0, column=1, padx=(0, 8))
        self.next_button = ttk.Button(actions, text=self.tr("next"), command=self.next_video, state="disabled", style="Secondary.TButton")
        self.next_button.grid(row=0, column=2, padx=(0, 8))
        ttk.Button(actions, text=self.tr("abort"), command=self.stop, style="Danger.TButton").grid(row=0, column=3)
        self.status_label = ttk.Label(root, textvariable=self.status, style="Status.TLabel", anchor="w")
        self.status_label.grid(row=5, column=0, sticky="ew")
        self.after(100, self.draw_funscript_graph)

    def clear_funscript_graph(self) -> None:
        self.graph_actions = []
        self.graph_duration_ms = 0
        self.graph_position_ms = 0
        if hasattr(self, "graph_canvas"):
            self.draw_funscript_graph()

    def load_funscript_graph(self, script: Path) -> None:
        try:
            raw = script.read_text(encoding="utf-8-sig").strip()
            decoder = json.JSONDecoder()
            idx = 0
            parsed = []
            while idx < len(raw):
                while idx < len(raw) and raw[idx].isspace():
                    idx += 1
                if idx >= len(raw):
                    break
                data, end = decoder.raw_decode(raw, idx)
                idx = end
                if not isinstance(data, dict):
                    continue
                for action in data.get("actions", []):
                    at = int(action.get("at", 0))
                    pos = max(0, min(100, int(action.get("pos", 0))))
                    parsed.append((at, pos))
            parsed.sort(key=lambda item: item[0])
            self.graph_actions = parsed
            self.graph_duration_ms = parsed[-1][0] if parsed else 0
            self.graph_position_ms = 0
        except (OSError, ValueError, TypeError, json.JSONDecodeError):
            self.clear_funscript_graph()
        self.draw_funscript_graph()

    def draw_funscript_graph(self) -> None:
        if not hasattr(self, "graph_canvas"):
            return
        c = self.graph_canvas
        c.delete("all")
        w = max(c.winfo_width(), 2)
        h = max(c.winfo_height(), 2)
        for fraction in (0.25, 0.50, 0.75):
            c.create_line(0, h * fraction, w, h * fraction, fill="#0D2940", dash=(2, 5))
            c.create_line(w * fraction, 0, w * fraction, h, fill="#091A2B")
        duration = self.graph_duration_ms
        if self.graph_actions and duration > 0:
            points = []
            for at, pos in self.graph_actions:
                points.extend(((at / duration) * w, h - 5 - (pos / 100.0) * (h - 10)))
            if len(points) >= 4:
                c.create_line(*points, fill="#00E5FF", width=2, smooth=False)
            cursor_x = min(max(self.graph_position_ms / duration, 0.0), 1.0) * w
            c.create_line(cursor_x, 0, cursor_x, h, fill="#FF3B8D", width=3)
        else:
            c.create_text(12, h / 2, text=self.tr("no_graph"), fill="#c4cad6", anchor="w", font=("Noto Sans", 10, "bold"))
            c.create_line(3, 0, 3, h, fill="#FF3B8D", width=3)

    def send_mpv_command(self, command: list) -> bool:
        if self.process is None or self.process.poll() is not None:
            self.set_status("Aucune vidéo en lecture.", "warning")
            return False
        if not self.mpv_socket.exists():
            self.set_status("Contrôle MPV indisponible : socket IPC absent.", "danger")
            return False
        payload = json.dumps({"command": command}).encode("utf-8") + b"\n"
        try:
            with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as client:
                client.settimeout(0.7)
                client.connect(str(self.mpv_socket))
                client.sendall(payload)
            return True
        except OSError as exc:
            self.set_status(f"Erreur de contrôle MPV : {exc}", "danger")
            return False

    def seek_relative(self, seconds: float) -> None:
        self.send_mpv_command(["seek", float(seconds), "relative+exact"])

    def toggle_pause(self, _event=None):
        self.send_mpv_command(["cycle", "pause"])
        return "break"

    def seek_from_graph(self, event):
        duration_ms = self.graph_duration_ms
        width = max(self.graph_canvas.winfo_width(), 1)
        if duration_ms <= 0:
            self.set_status("Durée de la vidéo inconnue.", "warning")
            return "break"
        ratio = min(max(event.x / width, 0.0), 1.0)
        seconds = duration_ms * ratio / 1000.0
        if self.send_mpv_command(["seek", seconds, "absolute+exact"]):
            self.graph_position_ms = int(seconds * 1000)
            self.draw_funscript_graph()
        return "break"

    def graph_mousewheel(self, event):
        if getattr(event, "num", None) == 4 or getattr(event, "delta", 0) > 0:
            self.seek_relative(5)
        else:
            self.seek_relative(-5)
        return "break"

    def update_graph_position(self) -> None:
        if self.process is not None and self.process.poll() is None:
            try:
                data = json.loads(self.progress_file.read_text(encoding="utf-8"))
                self.graph_position_ms = int(float(data.get("time_pos", 0.0)) * 1000)
                duration_ms = int(float(data.get("duration", 0.0)) * 1000)
                if duration_ms > 0:
                    self.graph_duration_ms = duration_ms
                self.draw_funscript_graph()
                now = __import__("time").monotonic()
                if self.current_video and now - self.last_position_save_time >= 5.0:
                    self.resume_positions[str(self.current_video.resolve())] = self.graph_position_ms
                    self.last_position_save_time = now
                    self.save_config()
            except (OSError, ValueError, TypeError, json.JSONDecodeError):
                pass
        self.after(80, self.update_graph_position)

    def add_scale(
        self, parent, row, label, variable, minimum, maximum, formatter
    ) -> None:
        ttk.Label(
            parent, text=label, style="CardText.TLabel"
        ).grid(row=row, column=0, sticky="w", pady=8)

        scale = ttk.Scale(
            parent,
            variable=variable,
            from_=minimum,
            to=maximum,
            orient="horizontal",
            style="Dark.Horizontal.TScale",
        )
        scale.grid(row=row, column=1, sticky="ew", padx=10, pady=8)

        value_label = ttk.Label(
            parent, width=9, anchor="e", style="Value.TLabel"
        )
        value_label.grid(row=row, column=2, sticky="e")

        def update(*_) -> None:
            value_label.configure(text=formatter(variable.get()))

        variable.trace_add("write", update)
        update()

    def set_status(self, text: str, kind: str = "neutral") -> None:
        color = {
            "neutral": COLORS["muted"],
            "success": COLORS["success"],
            "warning": COLORS["warning"],
            "danger": COLORS["danger"],
        }.get(kind, COLORS["muted"])
        self.status.set(text)
        ttk.Style(self).configure(
            "Status.TLabel",
            background=COLORS["panel_alt"],
            foreground=color,
            padding=(12, 9),
        )

    def _folder_videos(self, folder: Path) -> list[Path]:
        try:
            return sorted(
                [p for p in folder.iterdir() if p.is_file() and p.suffix.casefold() in VIDEO_EXTENSIONS],
                key=natural_key,
            )
        except OSError:
            return []

    def _set_selected_video(self, video: Path, announce: bool = True) -> bool:
        if not video.is_file():
            return False
        script = find_script(video)
        self.video_path.set(str(video))
        self.last_folder = str(video.parent)
        if self.playlist_folder is None or not self.playlist_folder.is_dir():
            self.playlist_folder = video.parent
        if script:
            self.script_path.set(f"✓  {script}")
            self.script_label.configure(foreground=COLORS["success"])
            self.launch_button.configure(state="normal")
            self.folder_button.configure(state="normal")
            self.next_button.configure(state="normal")
            self.load_funscript_graph(script)
            if self.resume_video_var.get():
                try:
                    self.graph_position_ms = int(self.resume_positions.get(str(video.resolve()), 0))
                except (TypeError, ValueError, OSError):
                    self.graph_position_ms = 0
                self.draw_funscript_graph()
            if announce:
                self.set_status(f"READY // {video.name}", "success")
            self.save_config()
            return True
        self.script_path.set("Aucun .funscript correspondant trouvé")
        self.script_label.configure(foreground=COLORS["danger"])
        self.launch_button.configure(state="disabled")
        self.folder_button.configure(state="disabled")
        self.next_button.configure(state="disabled")
        self.clear_funscript_graph()
        self.set_status("FUNSCRIPT NOT FOUND", "danger")
        self.save_config()
        return False

    def choose_video(self) -> None:
        initial = Path(self.last_folder) if Path(self.last_folder).is_dir() else Path.cwd()
        selected = filedialog.askopenfilename(title="Choisir une vidéo", initialdir=initial, filetypes=VIDEO_TYPES)
        if selected:
            self.playlist_folder = Path(selected).parent
            self._set_selected_video(Path(selected))

    def choose_folder(self) -> None:
        initial = Path(self.last_folder) if Path(self.last_folder).is_dir() else Path.cwd()
        selected = filedialog.askdirectory(title="Choisir un dossier vidéo", initialdir=initial)
        if not selected:
            return
        folder = Path(selected)
        self.playlist_folder = folder
        self.last_folder = str(folder)
        videos = [v for v in self._folder_videos(folder) if find_script(v)]
        if not videos:
            self.set_status("Aucune vidéo avec funscript dans ce dossier.", "warning")
            return
        self._set_selected_video(videos[0])
        self.set_status(f"DOSSIER CHARGÉ // {len(videos)} vidéo(s)", "success")

    def launch(
        self,
        video: Path | None = None,
        script: Path | None = None,
    ) -> None:
        if video is None:
            video = Path(self.video_path.get())
        if script is None:
            script = find_script(video)

        if not video.is_file() or script is None or not script.is_file():
            messagebox.showerror(
                "Fichier introuvable",
                "La vidéo ou son funscript n’existe plus.",
            )
            return

        if not PYTHON.is_file():
            messagebox.showerror(
                "Python introuvable",
                f"Environnement Python introuvable :\n{PYTHON}",
            )
            return

        if self.min_position.get() >= self.max_position.get():
            messagebox.showerror(
                "Réglages invalides",
                "La position minimale doit être inférieure à la position maximale.",
            )
            return

        ensure_internal_engine()

        if not self.playlist_active:
            self.stop()

        self.stop_requested = False
        self.current_video = video
        self.current_script = script
        self.load_funscript_graph(script)
        try:
            self.progress_file.unlink(missing_ok=True)
            self.mpv_socket.unlink(missing_ok=True)
        except OSError:
            pass
        self.save_config()

        amplification_factor = 1.0 + 2.0 * self.amplification.get() / 100.0
        effective_speed_multiplier = (
            self.speed_multiplier.get() * amplification_factor
        )

        start_ms = 0
        if self.resume_video_var.get():
            try:
                start_ms = int(self.resume_positions.get(str(video.resolve()), 0))
            except (TypeError, ValueError, OSError):
                start_ms = 0
            if self.graph_duration_ms > 0 and start_ms >= max(0, self.graph_duration_ms - 3000):
                start_ms = 0

        command = [
            str(PYTHON),
            str(PLAYER),
            str(video),
            str(script),
            "--min-position", f"{self.min_position.get():.3f}",
            "--max-position", f"{self.max_position.get():.3f}",
            "--speed-multiplier", f"{effective_speed_multiplier:.3f}",
            "--scan-seconds", "6.0",
            "--verbose",
            "--ipc-socket", str(self.mpv_socket),
            "--progress-file", str(self.progress_file),
            "--mpv-arg=--screen=1",
            "--mpv-arg=--fs-screen=1",
        ]
        if start_ms > 0:
            command.append(f"--mpv-arg=--start={start_ms / 1000.0:.3f}")

        if self.fullscreen.get():
            command.append("--mpv-arg=--fs")

        try:
            self.process = subprocess.Popen(command)
        except OSError as exc:
            messagebox.showerror("Erreur de lancement", str(exc))
            return

        self.set_status(
            f"Lecture Solace : {video.name} — amplification "
            f"{self.amplification.get():.0f} % "
            f"(vitesse finale x{effective_speed_multiplier:.2f}) "
            f"— PID {self.process.pid}",
            "success",
        )
        self.after(100, self.check_process)

    def next_video(self) -> None:
        video = self.current_video
        script = self.current_script

        if video is None:
            selected_text = self.video_path.get().strip()
            if selected_text:
                selected = Path(selected_text)
                if selected.is_file():
                    video = selected
                    script = find_script(selected)

        if video is None or not video.is_file():
            self.set_status("Aucune vidéo actuelle à passer.", "warning")
            return

        if not self.playlist_active:
            videos = sorted(
                [
                    path for path in video.parent.iterdir()
                    if path.is_file()
                    and path.suffix.casefold() in VIDEO_EXTENSIONS
                ],
                key=natural_key,
            )
            try:
                current_index = videos.index(video)
            except ValueError:
                self.set_status(
                    "La vidéo actuelle n’est plus dans son dossier.",
                    "warning",
                )
                return

            self.playlist = [
                candidate
                for candidate in videos[current_index + 1:]
                if find_script(candidate)
            ]
            self.playlist_active = bool(self.playlist)

        deleted_count = 0
        if self.delete_after_natural_end_var.get():
            deleted_count = len(self.delete_completed_files(video, script))

        if not self.playlist:
            self.playlist_active = False
            if self.process is not None and self.process.poll() is None:
                self.stop_requested = True
                self.process.terminate()
            if deleted_count:
                self.set_status(
                    f"{video.name} supprimée ({deleted_count} fichier(s)). "
                    "Aucune vidéo suivante.",
                    "success",
                )
            else:
                self.set_status("Aucune vidéo suivante disponible.", "warning")
            return

        self.manual_next_requested = True
        self.stop_requested = False

        if deleted_count:
            self.set_status(
                f"{video.name} supprimée ({deleted_count} fichier(s)). "
                "Passage à la suivante…",
                "success",
            )
        else:
            self.set_status("Passage à la vidéo suivante…", "neutral")

        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
        else:
            self.manual_next_requested = False
            self.current_video = None
            self.current_script = None
            self.after(50, self.play_next_in_playlist)

    def launch_folder_playlist(self) -> None:
        selected = Path(self.video_path.get())
        if not selected.is_file():
            messagebox.showerror(
                "Vidéo introuvable",
                "Choisis d’abord une vidéo valide.",
            )
            return

        folder = self.playlist_folder if self.playlist_folder and self.playlist_folder.is_dir() else selected.parent
        videos = self._folder_videos(folder)

        try:
            start_index = videos.index(selected)
        except ValueError:
            messagebox.showerror(
                "Erreur",
                "La vidéo sélectionnée n’est plus dans le dossier.",
            )
            return

        playlist = [
            video for video in videos[start_index:]
            if find_script(video)
        ]
        if not playlist:
            messagebox.showwarning(
                "Aucune vidéo lisible",
                "Aucune vidéo ne possède un funscript correspondant.",
            )
            return

        self.stop()
        self.playlist = playlist
        self.playlist_active = True
        self.delete_after_natural_end = self.delete_after_natural_end_var.get()
        self.stop_requested = False
        self.play_next_in_playlist()

    def play_next_in_playlist(self) -> None:
        while self.playlist:
            video = self.playlist.pop(0)
            script = find_script(video)
            if video.is_file() and script and script.is_file():
                self.video_path.set(str(video))
                self.script_path.set(f"✓  {script}")
                self.script_label.configure(foreground=COLORS["success"])
                self.load_funscript_graph(script)
                self.launch(video, script)
                return

        self.playlist_active = False
        self.delete_after_natural_end = False
        self.current_video = None
        self.current_script = None
        self.set_status(
            "Toutes les vidéos du dossier ont été traitées.",
            "success",
        )
        messagebox.showinfo(
            "Terminé",
            "La lecture du dossier est terminée.",
        )

    def delete_completed_files(
        self,
        video: Path,
        script: Path | None,
    ) -> list[str]:
        deleted = []
        errors = []
        targets = [
            video,
            *script_candidates_for_deletion(video, script),
        ]
        seen = set()

        for target in targets:
            try:
                key = target.resolve()
            except OSError:
                key = target.absolute()

            if key in seen:
                continue
            seen.add(key)

            if not target.is_file():
                continue

            try:
                target.unlink()
                deleted.append(str(target))
            except OSError as exc:
                errors.append(f"{target} : {exc}")

        if errors:
            messagebox.showwarning(
                "Suppression partielle",
                "Certains fichiers n’ont pas pu être supprimés :\n\n"
                + "\n".join(errors),
            )
        return deleted

    def check_process(self) -> None:
        if self.process is None:
            return

        code = self.process.poll()
        if code is None:
            self.after(100, self.check_process)
            return

        video = self.current_video
        script = self.current_script
        self.process = None

        if self.manual_next_requested:
            self.manual_next_requested = False
            self.current_video = None
            self.current_script = None

            if self.playlist_active and self.playlist:
                self.after(50, self.play_next_in_playlist)
            else:
                self.playlist_active = False
                self.set_status("Aucune vidéo suivante disponible.", "warning")
            return

        if code == 20:
            deleted_count = 0
            if video is not None:
                try:
                    self.resume_positions.pop(str(video.resolve()), None)
                    self.save_config()
                except OSError:
                    pass

            if (
                self.playlist_active
                and self.delete_after_natural_end_var.get()
                and not self.stop_requested
                and video is not None
            ):
                deleted = self.delete_completed_files(video, script)
                deleted_count = len(deleted)

            if (
                self.playlist_active
                and self.play_next_var.get()
                and not self.stop_requested
            ):
                if deleted_count:
                    self.set_status(
                        f"Fin naturelle : {video.name if video else 'vidéo'} supprimée "
                        f"({deleted_count} fichier(s)). Vidéo suivante…",
                        "success",
                    )
                else:
                    self.set_status(
                        "Fin naturelle. Vidéo suivante…",
                        "success",
                    )
                self.after(50, self.play_next_in_playlist)
            else:
                self.playlist_active = False
                self.playlist.clear()
                if deleted_count:
                    self.set_status(
                        f"Lecture terminée naturellement. "
                        f"{deleted_count} fichier(s) supprimé(s).",
                        "success",
                    )
                else:
                    self.set_status(
                        "Lecture terminée naturellement.",
                        "neutral",
                    )
        elif code == 0:
            self.set_status(
                "Lecture fermée avant la fin : rien n’a été supprimé.",
                "warning",
            )
            if self.playlist_active:
                self.playlist_active = False
                self.playlist.clear()
        else:
            self.set_status(
                f"Arrêt avec le code {code} : rien n’a été supprimé.",
                "danger",
            )
            if self.playlist_active:
                self.playlist_active = False
                self.playlist.clear()

        self.current_video = None
        self.current_script = None

    def stop(self) -> None:
        if self.current_video is not None and self.graph_position_ms > 0:
            try:
                self.resume_positions[str(self.current_video.resolve())] = int(self.graph_position_ms)
            except OSError:
                pass
        self.save_config()
        self.stop_requested = True
        self.manual_next_requested = False
        self.playlist_active = False
        self.delete_after_natural_end = False
        self.playlist.clear()
        if self.process is not None and self.process.poll() is None:
            self.process.terminate()
        self.process = None

    def load_config(self) -> None:
        try:
            data = json.loads(CONFIG.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return
        except Exception as exc:
            print(f"[Solace] Erreur lecture config {CONFIG}: {exc}", file=sys.stderr)
            return
        for key, var in (("min_position", self.min_position), ("max_position", self.max_position),
                         ("speed_multiplier", self.speed_multiplier), ("amplification", self.amplification)):
            try:
                var.set(float(data.get(key, var.get())))
            except (TypeError, ValueError):
                pass
        self.fullscreen.set(bool(data.get("fullscreen", self.fullscreen.get())))
        self.delete_after_natural_end_var.set(bool(data.get("delete_after_natural_end", self.delete_after_natural_end_var.get())))
        self.play_next_var.set(bool(data.get("play_next", self.play_next_var.get())))
        self.resume_video_var.set(bool(data.get("resume_video", self.resume_video_var.get())))
        language = str(data.get("language", "fr")).lower()
        self.language.set(language if language in ("fr", "en") else "fr")
        self.last_folder = str(data.get("last_folder") or self.last_folder)
        pf = str(data.get("playlist_folder") or "")
        if pf and Path(pf).is_dir():
            self.playlist_folder = Path(pf)
        rp = data.get("resume_positions", {})
        if isinstance(rp, dict):
            self.resume_positions = rp
        video_text = str(data.get("video", "") or "").strip()
        self.video_path.set(video_text)
        if video_text and Path(video_text).is_file():
            self.saved_video_on_startup = Path(video_text)
            if self.playlist_folder is None:
                self.playlist_folder = Path(video_text).parent
            self.last_folder = str(Path(video_text).parent)

    def _restore_last_video(self) -> None:
        video = self.saved_video_on_startup
        if video is not None and video.is_file() and self._set_selected_video(video, announce=False):
            self.set_status(f"RESTORED // {video.name}", "success")

    def save_config(self) -> None:
        try:
            CONFIG.parent.mkdir(parents=True, exist_ok=True)
            video_text = str(self.current_video) if self.current_video else self.video_path.get().strip()
            data = {
                "min_position": self.min_position.get(),
                "max_position": self.max_position.get(),
                "speed_multiplier": self.speed_multiplier.get(),
                "amplification": self.amplification.get(),
                "fullscreen": self.fullscreen.get(),
                "delete_after_natural_end": self.delete_after_natural_end_var.get(),
                "play_next": self.play_next_var.get(),
                "resume_video": self.resume_video_var.get(),
                "language": self.language.get(),
                "video": video_text,
                "last_folder": self.last_folder,
                "playlist_folder": str(self.playlist_folder) if self.playlist_folder else "",
                "resume_positions": self.resume_positions,
            }
            tmp = CONFIG.with_suffix(CONFIG.suffix + ".tmp")
            tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
            tmp.replace(CONFIG)
        except Exception as exc:
            print(f"[Solace] Erreur sauvegarde config {CONFIG}: {exc}", file=sys.stderr)

    def on_close(self) -> None:
        self.stop()
        self.save_config()
        for path in (self.progress_file, self.mpv_socket):
            try:
                path.unlink(missing_ok=True)
            except OSError:
                pass
        self.destroy()


def main() -> None:
    app = SolacePlayerGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
