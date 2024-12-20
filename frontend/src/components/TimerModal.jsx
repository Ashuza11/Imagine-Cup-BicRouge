import { CircleAlert } from "lucide-react";
import { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";

/**
 * `sec` est le nombre de séconde du compte à rebours
 * `onCountDown` est la fonction à executer quand le compte arrive à 0
 * @param {{onCountDown?:()=>void, sec:number}}
 * @returns
 */
const TimerModal = ({ onCountDown, sec } = {}) => {
    const [isWindowActive, setIsWindowActive] = useState(true);
    const [root, setRoot] = useState(null);

    useEffect(() => {
        /**
         * Function that helps handle student switching windows
         * before submittion
         * @param {FocusEvent} event
         */
        const handleWindowsBlur = (event) => {
            event.target.focus();
            setIsWindowActive(false);
        };
        const handleWindowsFocus = (event) => {
            event.target.focus();
            setIsWindowActive(true);
        };
        const handleWindowsChange = () => {
            if (document.hidden) setIsWindowActive(false);
        };

        window.addEventListener("blur", handleWindowsBlur);
        window.addEventListener("focus", handleWindowsFocus);
        document.addEventListener("visibilitychange", handleWindowsChange);

        return () => {
            window.removeEventListener("blur", handleWindowsBlur);
            window.removeEventListener("focus", handleWindowsFocus);
            document.removeEventListener(
                "visibilitychange",
                handleWindowsChange
            );
        };
    }, []);

    useEffect(() => {
        // Dans ce useEffect nous montons le modal sur la page
        // en utilsant une hierrarchy react parrallele
        const modal = document.createElement("div");
        modal.classList.add("timer-modal");
        document.body.appendChild(modal);
        const root = createRoot(modal);
        setRoot(root);

        return () => modal.remove();
    }, []);

    useEffect(() => {
        if (!root) return;
        root.render(
            <Modal
                onCountDown={onCountDown}
                sec={sec}
                isActive={!isWindowActive}
            />
        );
    }, [onCountDown, sec, isWindowActive, root]);

    return <></>;
};

/**
 * @param {{onCountDown?:()=>void, sec:number,isActive:boolean}}
 * @returns
 */
const Modal = ({ onCountDown, sec, isActive } = {}) => {
    const [count, setCount] = useState(sec ?? 60);
    const numberFormat = Intl.NumberFormat("fr-FR", {
        minimumIntegerDigits: 2,
    });
    const timeFormat = (sec = 0) => {
        return `${numberFormat.format(
            Math.floor(sec / 60)
        )}:${numberFormat.format(sec % 60)}`;
    };

    useEffect(() => {
        let timer;
        const countDown = () => {
            setCount((t) => {
                if (t - 1 <= 0) {
                    if (onCountDown) onCountDown();
                    clearInterval(timer);
                    return 0;
                } else return t - 1;
            });
        };
        if (isActive) timer = setInterval(countDown, 1000);

        return () => clearInterval(timer);
    }, [onCountDown, isActive]);

    return (
        <div
            style={{ display: isActive ? "block" : "none" }}
            className="absolute top-0 bottom-0 right-0 left-0 z-[9999] bg-[#5050501f] backdrop-blur-[1px]"
        >
            <div className="w-full h-full flex justify-center items-center">
                <div className="px-[2rem] py-[1rem] bg-[#fefefe] rounded-lg shadow-xl">
                    <header className="flex gap-2 items-center justify-center">
                        <span className="">
                            <CircleAlert size={"2rem"} />
                        </span>
                        <span className="font-medium text-lg">
                            Vous avez quitté la fenêtre de l&apos;évaluation
                        </span>
                    </header>

                    <div className="py-[.3rem]" />

                    <hr />

                    <div className="py-[.3rem]" />

                    <section>
                        <div className="text-[3rem] text-center font-bold text-red-600">
                            {timeFormat(count)}{" "}
                        </div>

                        <div className="py-1 bg-neutral-300 rounded-full">
                            <div className="bg-red-300 duration-[]"></div>
                        </div>

                        <p className="text-red-600 text-[85%] text-center italic">
                            Votre copie sera remise comme telle si le chrono
                            arrive à <span className="font-bold">00:00</span>
                        </p>
                    </section>
                </div>
            </div>
        </div>
    );
};

export default TimerModal;
