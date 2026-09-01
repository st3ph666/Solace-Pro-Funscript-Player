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
APP_VERSION = "v1.1.0-BLE-direct"
APP_NAME = f"Solace Funscript Player {APP_VERSION}"
PYTHON = Path.home() / "buttplug-player-venv/bin/python"
CONFIG = Path.home() / ".config/solace-player-gui.json"
VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov", ".webm", ".m4v"}
VIDEO_TYPES = (
    ("Vidéos", "*.mp4 *.mkv *.avi *.mov *.webm *.m4v"),
    ("Tous les fichiers", "*"),
)

COLORS = {
    "bg": "#111318",
    "panel": "#191c22",
    "panel_alt": "#20242c",
    "border": "#2c313b",
    "text": "#f2f4f8",
    "muted": "#9aa3b2",
    "accent": "#7c5cff",
    "accent_hover": "#9278ff",
    "success": "#39d98a",
    "warning": "#ffb84d",
    "danger": "#ff5c72",
    "track": "#343a46",
}

ENGINE_BUNDLE = 'c-pNy+iu**a_{pMeYgmg;~i2nl4b0foLRtY$cb=luV6V&0Ifju40}e5IV96f>H-}t_BGGR2jnS;kx$6m@t^FMq^d7ulWbD*Ci7sE?5gVO>biI9n?D>>f*-7t?0{w0q_``u^6Y4`<@ugO(Y7ip&Z3AU`y%Hhp;?xfv`q3$OeW?V-xZV#R=<n8Y?I{Xb)5*dDb3qIi##*WxiC*6*=01X-}22TR%3{2UGRLvL<4<SKbCA?Y?HK}yG-^>@m|pKDoxgg@iTZ;1La+jWIOZyWp+22l>BZvA@Gv`>y*(?X8cEdd6gzCD`)EEd;>yYe8O%wtSHH;ggfCp=ZZ$bldSaRBmTU%d0eH8oJqlwzy7zT|JVN^bS;2v_;cnp(5IOwX_~SCP-2=1^2@=xD$63Rc0rNSJH~@++$Va?He}gCB?GW>Z;PZLiK0z{pelBp#!Ru|&1xDb$`yz=6lKgfR|8Y|FQ>4N<or&6$WLyQ(m$L|Cg(rBdHL!jIzM^;@$}URSrPB~;q%3OK3@d$`QcIUd>uaz*6a8<pfCP-IA_l{$1jeLJcIX-?@vG2Scl_SuU@|Tdj!Y546pJ%^QYv1c;P0`w#n{5<SE^-0F)(wbp;!`xnd#en>U$EHYpW?ye+Oz&t9p0irE$vJjs$WihRM+?My3PgsQWYvrI|w19_KcY*~v4Awvrg__5ylU`su$amZgJJ;1{M+TiPIyJZ}P)}GfM;p|^3Cdw#@VRSx`gVN08Dq#H?n3!G!nm}HaOR`OKS_1rH9?o40DJjQcgb(*Q*ma&I8-H2@++2Y+^oB{GG5=K0RAb;T+4e*fvfD(I!k@MwB@+NuOHkwZ`t9ZG=pWvl{*&33@cgG&e~!*SygzyQcIqS)3RbRDcmVtMU(-~uK3r|;-5<T7N$tDB9k9-;ECWhWn&*W-mCQv()J_tH58$}uepd=pCyx7TjjLtj1mX;QbJiQue(9%k%O^RdwMlcq{5At^DTtJ@!Uy#^ZlIJO_@K64PT_m#1BFP|=(89wZ!{8=nO1uH$lJ4zp*QX6u4Dq&>rhc!mq;QAC}9VpB`oKPY*9*+>lx2}PqSDXkA7Q{6g2h%g2Sa`3m%5K>T{%I^hyZ<Vx<-nNPvL*Az<YDFQ02+xUBp;Fxy7tw)J-)YoLPOfxROHy1X#1_JwGx>Aj~{=Pk`TXT)nr!RO}XVb+l%gm_x!T&#R=<^kT)n>HZRkY$@ZMu+?zcrOe~ldm%@h=ei3rp9V!W<{2ilt=o&tB$<YcR8=rktDMnYTpE6T2c_y(>UX7b8WNr;`sRJMc-^eD{yKg?Y6lQrJ!0R2&_UoJI~?btQZ0MfityW(j;TEP9(A3LQ$j;wxyJ2WYMP2nJ6HqV@7>Y@WMxmVa(LdPP=a2;GpDuTaTt>wX#%c>5^3&nV~EI?+=g*h-!n$o;N1N_f>|$M~M)ft&`leFGJ-sJF}xC`<@B)0dk3g@$yc4hm7vo5}kYBDQLn<rKHr2W4Z8bN}i%}IjwV&Hy~unUssvf@T4dQlat4@5-RmdXy;W{ManJ`%v<4~%S+hWi_10w%Fuu#i~}S>P4HFxYB-Z0pTL$jG)tvqKEN4`qmtd0zH}R4aVxJXx54)T6at>LZL+S2+iY!fh$?cWXy-VC+C{y35b(uiC)02SeVH3!s;&?(JX(5}eT{+025@_N>(6IopJYBHs<RdzKmcM#*>n{4|IF^Bmd?nByMpP*k2I~+vm+&f*jXl7#k%GO{QdyRUmrmUDWpXKKGgRqY&fvglOnh;Uiy|dt+E76v@hHQGJF)RLhEIB8VyuiKVAfj%ZvFX8a<-IW1q(ck|?OQupm_%!ZGVYB#U`qBxRYeV5X3a9=bwsBWT}y!^qYc8HsZ+Q<OBz5}BmzbEu9$xvN{PT%sSJ^#H6uP3tfwl;$l80|j}DQdFRqjq$+VBuFQsCS%`&4T3^R`;kd|E7#Zy@~2gc0ifR#vi3g`-R}Y~EWK6~f9OzDTliFx2#quwqVX-3Ewa)N)qfFBc2^otiU!x&uu*~$6?4*I1L*{0(dc8j0I-Dv?9yIPxj+$>^AY}wg~cw%4h9hQK@tJrVHv5wfRg;s_3OaucLa#QXaV5Q6bbO*y(%nHWvDMUG=r=LzQ#h=VseA6hJs>O)~Rts;~1inunR*yg7L!s-12694=bzWVHaz=*WT2YH&x%f9<b)7fy56QOgp_3`5)}m(sDsUDEY&7wWnRSJ$s2Q9ht&$n(dem3h?|X?!41>v42}nW?i=!GU9||VS*-qE;oum-nGwpA|U;`Z*%rQya9T@{rc|&TnBc-t{J)4Og|hP{r2mB_Hp__Wh3_=#As=Q-=4gWq;d;|8k#~>*Wjzgd^#YKt)~~NQDB|d300dw{Cj&_LH^%nIXZuYt-gJjy7EwM5{eO5(5v?!vMKzw9OUfFzry4j&C8P91Mq`4wDNXUx(JW8ML$Jt9NMw<-ZPk%<J3RCInnBH@aE$=!GJ?yf9_jGyn7&`qY+Qlgl0)GyG}MTPN+rMEyXZS#3sLHyxvuNe#?Ks*Ej(SRPm<8Q7pv~%hX6s)s5eADEAuUci&vpU|2!S<yZh=r$^i*<rT!wkLQ77Z(uf0wevhVX^X(bZ3dUEINq$Ltte{Gyf+{btW4rBpG&E}f-F0H)Jq;BW$PRPAAYacd?5H_tlf_H`1^)H%AjrMjOUOuY^ptMH5ici78~Ii44_ngTpWfi%!Un>boF@o#O_up-LGRx;w5o=tvSlZ*Sm#M_NGRxm}+@?W>02MWHECRvC(IbIHqYwkyh3^AUT-0gn9PmGvrfO_%9}f;6zhZ-DV)A<)EA&^@TOGt35U10y`V{5gFSij39F<Iz3KNg}~jHl3|mKWh{l-8|qcUzkJ4L+-O)OXd67R&h}nGW(*A9_e*prMK@tpCGixZ@lDSJjIs*G(Ke;Zs>SFp!U?`n9SsQ);_MWAYq*9@8{wgA>~^EwaAaB}av96<Fe5#Z60;)^^lR~fcv<T~CPgm3{8!8{CvfhGWpYFD_ugLDL+A>*txqZ^f`SIuwEqN2fUjP}3cE=&B0JPk{z<-09k@3f3J{f0^(M0#ZufQKv?R3-&xlHrmf9R2uzrkT_SNCEZ<O79Z8l=0?NB@!kC(<g#<tC~gbx<Z^Xi(eQx=lfjDsIJ1)QynlG-W1XZySa`B}$MG)=)xVk^s{#gt(QK@+C8Yud`5vHurQu}KnNt!CLidaE0=ru)(~8d?gg_Gt%kI70nyR%UBVBT`M)v@bo$f!*0OouZXIPnZpHZv2Rw`MTtrM~nHqDfXH*7>I#ZLz{r<HJD~oM{+YTkk{v|JO@cE?+xn1-(q~5Ajc`KvdvYrFRuOTBxbp4-#CuH&@M_&Bg%KCO$6dsE%D}9HayEAVbaBnl4mO|@n9lLi@hMo@&No7tdOSd0dRI37Tkb!<TtB3CfcK)K#v2QYnA2pp(P9@Sy7ciQfvZrlZ>zKt;IZ8z|Wc$%_g?nmXgpLuVS4xuI@s8y~ef{;CZW`7rFswj>N-vVD6#-E08ivOwA`J(<hk*D^whW?6v^vm5>P-s9&C5n==j7yfDX(E#$hjF-Txyb*bf4VIm?t@b!Cn^49y9K)Tg(0T|6C8c4HyPTVV(7xrWp*JD%G9nkKq7XH)b?pMi8<7d_FxB3=&cNN>KVhqRNJ6Xjo;--RmGLv=gQy2GOE0I<=`!i^^{hCprLeq#zQ<JVqfkCdqc~z9MX=(z%$u*`_S_ANC!y4<KdNiFX)4~@ees>(tHM8N-t8dj~BH3Yz;j4=s;rZ#`oxb}pBhBlFllN~eCFqs($P32LNTEbmpwcO5G`!AQj5VUw`}Qs`Pxpn&;8^T91Z{c|tyy)s@fPBM{<5?q7?y~tc|fq{Gm((I`{^C2$|S`Gf|c3!wYsOu)A8!`ETubU7`Zog4o<TUHqS7ag!ApgZ@>Oqw=QiE=xrZ?{Ec0kPI{@h4yo;qmZ3OMl!CPz2+-C@`QOe-ZR^@Z%YQW}Z3i|P?h#{IT3-N?o;Lo#@HP(RcdyaOI7&daO>S2hkOF;ML~UsRCM&9~9F)g=@E)_2l}sjt?F<b4LAfv7ml-<C12~!TS#s*Bx_wik%F-nJ<oA>s*8__EI<K;EmG1kHZnSU3`B}YZhy-EFY7|SCqi)Rj&U*|>O8_oxYJ{fIQOOo*7MWPry6=)wG+$6Q)J>TX4P1;dfN_M`D&Bqx=k39QR)Vz-_f_q8mR5r7xXMO!%w_@tHGJMeG72sv!wQ{1W(*L&JfD-j2)mhKB%RzfO?7705<Bp+_`aQ=W7;+k7l)9z!6?u?Pzhalc-+WZ6pY2uzDmoa0F&cW`zU?#h+8n3BDw{W=8-wL0Fx~;UVv^(7;~01>-DY7vLM9%a^GDm`U&kQ_QKW0GOZcd^NP#X%${;g@bNNR@4#Nwn@y~MBtV9X-qDh!xFM_|g`hKd>jQsl4oUXp3B6%d5mbY9o~M4Jwyh&xPeOT)Lu1suNSy-?;UY+Y2Z5c!)AZch#^Ag(Vt&_nW;HUEq2;-+4#8}S!l>j1tyCR@ND7Xn4BnoCSx05d@@)W{g{@|g@Gw8^#HQza#}65L9`WnYeun}!O8AtPH8_N$>F{}P*BWZI8&sEpNe-Vn$=*8Jmg$N*1Jm>3F&8=lywhVmSH9hX=|+1o?Xhb>Kz=*yddNh7`E(U3x+y`6kXzXyyaHAcVk!`+0PYu|dH}Ay5CFVE)X}DntGP1>Bnwm{H*ZNgf}D*b))s9LJ5~w#G+yC+go<)<Ktmd$dK<xc7#SOHL5*KsM7eTS$c(X={;u1J?QBM?m*cFW=TwcM_6-HxNmsdl(5fGT@^?rDAn&8jfttf<Ih<7sCd+SJ_iMW=Q(M(1|4kF#u`yj`tWIO_nq}QGD)J1%uxwzvh+xYVa~_sm=XZ?Ts6r*ZCHe9nkV_>3GH&eKVN0))w<2I8a}oB4w(>5glm5TDKTdCS#I39A(7reU4hS+U@J?1XC_Nh97Qx+c)l1+J4BclAeR5Sypb9QZBQ4nyl4w>A^zk_6@4ja8nc{zn?YwqDaFthSEVEv`q~I36NuEt~a2?FiweU4RK^se|ziVaKHO+QTYCh_7(8<W#gg|lvoOQNw60p<;nC=%=J<G5KA<ruZIp}7vL$T7;texpSn?54wm4+Jxt7{Zs)0qa=oj%6bxfsYNMlLd_)ct3E-|=P3KZZwJJe~f_z=?@Mtd;s+Eo6BVKRkjW@``U5xz~0h8wkhYLUs_w;zzvlM#i_`kFM0o%RpqA47!`9+4YF8nSbwYPB?|Hgl=CEQhmBZc?xSgdep<Af<_(1>c7u;avSmIOg9q0x_!9C4tm<YnvP}rV9x5k2-%eJj{EbE=gsYK-Oi$IR;1|M8TJ!7wUPA!Lizu|uWoyNoz!YP+<o)+4)NIEmOOT(`n8<vBHZdxE>)NE%jf#4Pgo!Ntg8fEsXUe7s+n6KQoQ6ld9mS44(bCb`HW?#8%p!8z+|JA>T%zbNt8DNP{;H!pdi3TW1t(2U=-zD!B*1qVRLRvtF&Cb2<M|DP{o3MjV*6O8{ETjR8{H>A&=vNW(LOF4sbqygmZ|ckC9kBLPEBgf~L*%JIUCK2~>LE6v^Vz_2}GSP$G})i1yrot}cSEJW=Kx3OEQP<C=sGUwF4L)vaQ$nf>B&l!823lugj_nM~0dpbOWa<_@XE(B`<OkQcTO1$BVJHdV`3L-`<&EVb2H(X5r<c2Y6(y?4e@_YeU)*;7dQ0kft8sPbd@gg|s?FVKWwUS+<09*X(xB*8yuz*cw^$?Ho|gd&I{{dXR{KQC1Rnoj-~%w#|p'


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
        self.geometry("1000x700")
        self.minsize(700, 520)
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

        self.process: subprocess.Popen | None = None
        self.playlist: list[Path] = []
        self.playlist_active = False
        self.delete_after_natural_end = False
        self.stop_requested = False
        self.manual_next_requested = False
        self.current_video: Path | None = None
        self.current_script: Path | None = None
        self.graph_actions: list[tuple[int, int]] = []
        self.graph_duration_ms = 0
        self.graph_position_ms = 0
        self.progress_file = Path(tempfile.gettempdir()) / f"solace-player-progress-{os.getpid()}.json"
        self.mpv_socket = Path(tempfile.gettempdir()) / f"solace-player-mpv-{os.getpid()}.sock"

        self.configure_styles()
        self.load_config()
        ensure_internal_engine()
        self.build_ui()
        self.after(150, self.update_graph_position)
        self.protocol("WM_DELETE_WINDOW", self.on_close)

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
            font=("Noto Sans", 22, "bold"),
        )
        style.configure(
            "Subtitle.TLabel",
            background=COLORS["bg"],
            foreground=COLORS["muted"],
        )
        style.configure(
            "CardTitle.TLabel",
            background=COLORS["panel"],
            foreground=COLORS["text"],
            font=("Noto Sans", 12, "bold"),
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
            font=("Noto Sans", 10, "bold"),
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
            font=("Noto Sans", 10, "bold"),
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
        shell = ttk.Frame(self, style="Root.TFrame")
        shell.pack(fill="both", expand=True)

        graph_frame = tk.Frame(
            shell, bg="#050609", height=145,
            highlightbackground=COLORS["border"], highlightthickness=1,
        )
        graph_frame.pack(side="bottom", fill="x")
        graph_frame.pack_propagate(False)

        graph_header = tk.Frame(graph_frame, bg="#050609", height=30)
        graph_header.pack(side="top", fill="x")
        graph_header.pack_propagate(False)

        tk.Label(
            graph_header,
            text="MOUVEMENT FUNSCRIPT — clique ou glisse pour déplacer la vidéo",
            bg="#050609", fg="#b9c0cc",
            font=("Noto Sans", 8, "bold"), padx=10, anchor="w",
        ).pack(side="left", fill="x", expand=True)

        for label, command in (
            ("−10 s", lambda: self.seek_relative(-10)),
            ("Pause / Reprendre", self.toggle_pause),
            ("+10 s", lambda: self.seek_relative(10)),
        ):
            tk.Button(
                graph_header, text=label, command=command,
                bg=COLORS["panel_alt"], fg=COLORS["text"],
                activebackground=COLORS["accent"], activeforeground="white",
                relief="flat", bd=0, padx=12, pady=3, cursor="hand2",
            ).pack(side="left", padx=2, pady=3)

        self.graph_canvas = tk.Canvas(
            graph_frame, bg="#090b10", highlightthickness=0,
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
        ttk.Label(header, text="Solace Funscript Player", style="Header.TLabel").grid(row=0, column=0, sticky="w")
        ttk.Label(
            header, text=APP_VERSION, style="Subtitle.TLabel"
        ).grid(row=0, column=1, sticky="e", padx=(12, 0))
        ttk.Label(
            root, text="Lecture MPV + funscript — Solace Pro BLE direct, sans Intiface",
            style="Subtitle.TLabel",
        ).grid(row=1, column=0, sticky="w", pady=(4, 18))

        file_card = ttk.Frame(root, style="Card.TFrame", padding=18)
        file_card.grid(row=2, column=0, sticky="ew", pady=(0, 14))
        file_card.columnconfigure(1, weight=1)
        ttk.Label(file_card, text="Sélection", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))
        ttk.Label(file_card, text="Vidéo", style="CardText.TLabel").grid(row=1, column=0, sticky="w", pady=6)
        ttk.Entry(file_card, textvariable=self.video_path, state="readonly", style="Dark.TEntry").grid(row=1, column=1, sticky="ew", padx=10, pady=6)
        ttk.Button(file_card, text="Parcourir", style="Secondary.TButton", command=self.choose_video).grid(row=1, column=2, pady=6)
        ttk.Label(file_card, text="Funscript", style="CardText.TLabel").grid(row=2, column=0, sticky="nw", pady=6)
        self.script_label = ttk.Label(file_card, textvariable=self.script_path, style="CardText.TLabel", wraplength=650)
        self.script_label.grid(row=2, column=1, columnspan=2, sticky="w", padx=10, pady=6)

        settings = ttk.Frame(root, style="Card.TFrame", padding=18)
        settings.grid(row=3, column=0, sticky="ew", pady=(0, 14))
        settings.columnconfigure(1, weight=1)
        ttk.Label(settings, text="Réglages Solace", style="CardTitle.TLabel").grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 12))
        self.add_scale(settings, 1, "Position minimale", self.min_position, 0.0, 0.90, lambda value: f"{float(value) * 100:.0f} %")
        self.add_scale(settings, 2, "Position maximale", self.max_position, 0.10, 1.0, lambda value: f"{float(value) * 100:.0f} %")
        self.add_scale(settings, 3, "Réactivité BLE", self.speed_multiplier, 0.25, 2.0, lambda value: f"{float(value):.2f} ×")
        self.add_scale(
            settings,
            4,
            "Amplification adaptateur",
            self.amplification,
            0,
            100,
            lambda value: (
                f"{float(value):.0f} %  "
                f"(x{1.0 + 2.0 * float(value) / 100.0:.2f})"
            ),
        )
        ttk.Checkbutton(
            settings, text="Ouvrir MPV en plein écran sur l’écran de droite",
            variable=self.fullscreen, style="Dark.TCheckbutton",
        ).grid(row=5, column=1, sticky="w", padx=10, pady=(10, 2))

        ttk.Checkbutton(
            settings,
            text="Supprimer la vidéo et son funscript à la fin ou en passant à la suivante",
            variable=self.delete_after_natural_end_var,
            style="Dark.TCheckbutton",
        ).grid(row=6, column=1, sticky="w", padx=10, pady=(6, 2))

        ttk.Checkbutton(
            settings,
            text="Passer automatiquement à la vidéo suivante",
            variable=self.play_next_var,
            style="Dark.TCheckbutton",
        ).grid(row=7, column=1, sticky="w", padx=10, pady=(6, 2))

        actions = ttk.Frame(root, style="Root.TFrame")
        actions.grid(row=4, column=0, sticky="ew", pady=(0, 14))
        actions.columnconfigure(0, weight=1)
        self.launch_button = ttk.Button(actions, text="▶  Lancer la vidéo", command=self.launch, state="disabled", style="Accent.TButton")
        self.launch_button.grid(row=0, column=0, sticky="ew", padx=(0, 8))
        self.folder_button = ttk.Button(actions, text="⏭  Lire le dossier", command=self.launch_folder_playlist, state="disabled", style="Secondary.TButton")
        self.folder_button.grid(row=0, column=1, padx=(0, 8))
        self.next_button = ttk.Button(actions, text="⏩  Vidéo suivante", command=self.next_video, state="disabled", style="Secondary.TButton")
        self.next_button.grid(row=0, column=2, padx=(0, 8))
        ttk.Button(actions, text="■  Arrêter", command=self.stop, style="Danger.TButton").grid(row=0, column=3)
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
            data = json.loads(script.read_text(encoding="utf-8"))
            parsed = []
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
            c.create_line(0, h * fraction, w, h * fraction, fill="#262b36", dash=(3, 5))
            c.create_line(w * fraction, 0, w * fraction, h, fill="#171b23")
        duration = self.graph_duration_ms
        if self.graph_actions and duration > 0:
            points = []
            for at, pos in self.graph_actions:
                points.extend(((at / duration) * w, h - 5 - (pos / 100.0) * (h - 10)))
            if len(points) >= 4:
                c.create_line(*points, fill="#b39cff", width=2, smooth=False)
            cursor_x = min(max(self.graph_position_ms / duration, 0.0), 1.0) * w
            c.create_line(cursor_x, 0, cursor_x, h, fill="#ff263f", width=4)
        else:
            c.create_text(12, h / 2, text="Choisis une vidéo avec son funscript", fill="#c4cad6", anchor="w", font=("Noto Sans", 10, "bold"))
            c.create_line(3, 0, 3, h, fill="#ff263f", width=4)

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

    def choose_video(self) -> None:
        initial = Path(self.video_path.get()).parent             if self.video_path.get() else Path.cwd()

        selected = filedialog.askopenfilename(
            title="Choisir une vidéo",
            initialdir=initial,
            filetypes=VIDEO_TYPES,
        )
        if not selected:
            return

        video = Path(selected)
        script = find_script(video)
        self.video_path.set(str(video))

        if script:
            self.script_path.set(f"✓  {script}")
            self.script_label.configure(foreground=COLORS["success"])
            self.launch_button.configure(state="normal")
            self.folder_button.configure(state="normal")
            self.next_button.configure(state="normal")
            self.load_funscript_graph(script)
            self.set_status(
                f"Funscript trouvé : {script.name}",
                "success",
            )
        else:
            self.script_path.set("Aucun .funscript correspondant trouvé")
            self.script_label.configure(foreground=COLORS["danger"])
            self.launch_button.configure(state="disabled")
            self.folder_button.configure(state="disabled")
            self.next_button.configure(state="disabled")
            self.clear_funscript_graph()
            self.set_status("Funscript introuvable.", "danger")

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

        videos = sorted(
            [
                path for path in selected.parent.iterdir()
                if path.is_file()
                and path.suffix.casefold() in VIDEO_EXTENSIONS
            ],
            key=natural_key,
        )

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
        except (OSError, json.JSONDecodeError):
            return

        self.min_position.set(
            float(data.get("min_position", self.min_position.get()))
        )
        self.max_position.set(
            float(data.get("max_position", self.max_position.get()))
        )
        self.speed_multiplier.set(
            float(data.get("speed_multiplier", self.speed_multiplier.get()))
        )
        self.amplification.set(
            float(data.get("amplification", self.amplification.get()))
        )
        self.fullscreen.set(
            bool(data.get("fullscreen", self.fullscreen.get()))
        )
        self.delete_after_natural_end_var.set(
            bool(data.get("delete_after_natural_end", self.delete_after_natural_end_var.get()))
        )
        self.play_next_var.set(
            bool(data.get("play_next", self.play_next_var.get()))
        )

    def save_config(self) -> None:
        CONFIG.parent.mkdir(parents=True, exist_ok=True)
        data = {
            "min_position": self.min_position.get(),
            "max_position": self.max_position.get(),
            "speed_multiplier": self.speed_multiplier.get(),
            "amplification": self.amplification.get(),
            "fullscreen": self.fullscreen.get(),
            "delete_after_natural_end": self.delete_after_natural_end_var.get(),
            "play_next": self.play_next_var.get(),
        }
        CONFIG.write_text(
            json.dumps(data, indent=2),
            encoding="utf-8",
        )

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
