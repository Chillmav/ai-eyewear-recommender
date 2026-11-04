import { useState, useEffect, useRef } from 'react'
import { useNavigate } from 'react-router-dom';
import Preferences from '../Components/Preferences';

export default function LogPage({ setUser }) {

    
    const [showPopup, setShowPopup] = useState(false);

    const [preferences, setPreferences] = useState({});
    useEffect(() => {

        console.log("Fetching frames")
        fetch("http://localhost:8000/frames", {
            method: "GET"
        })
        .then(res => res.json())
        .then(data => {
            setPreferences(data)
            console.log(data)
        }
        )
        
    }, [])
    

    const [userPreferences, setUserPreferences] = useState(

        {

            AI: 50,
            Shape: [],
            Mark: [],
            Type: [],
            Color: []

        }

    );

    const [userImportances, setUserImportances] = useState({

        Mark: 2.5,
        Color: 2.5

    })

    const navigate = useNavigate();
    const [isloggedIn, setIsLoggedIn] = useState(false)

    function login() {

        for (let preference of Object.keys(userPreferences)) {
            if (!userPreferences[preference].length && !Number(userPreferences[preference])) {

                console.error('You didn’t choose all your preferences');
                setShowPopup(true);
                return 0;

            } 
        }
        setIsLoggedIn(true);

    }

    useEffect(() => {

        if (isloggedIn) {
            setUser([userPreferences, userImportances]);
            navigate('/Cam');
        }
        
    }, [isloggedIn])

    if (preferences.Shape) {

        return (

        <div className='flex flex-col rounded-2xl'>

            <Preferences
            preferences={preferences}
            userPreferences={userPreferences}
            setUserPreferences={setUserPreferences}
            userImportances={userImportances}
            setUserImportances={setUserImportances}
            />

            <button className='bg-[#DDE5B6] rounded-2xl w-[50%] m-auto mb-[20px] cursor-pointer text-[20px] p-[5px]' onClick={() => login()}>
                Potwierdź
            </button>

            {showPopup && (
            <div className="fixed inset-0 bg-white/10 backdrop-blur-[1px] flex items-center justify-center z-50">
                <div className="bg-[#F7F6F3] text-[#555B4F] p-6 rounded-2xl shadow-xl max-w-md text-center backdrop-blur-sm border border-gray-300">

                    <p className="text-lg text-[#555B4F] mb-4">Musisz wybrać wszystkie preferencje aby przejść dalej</p>
                    <button
                    onClick={() => setShowPopup(false)}
                    className="mt-2 px-4 py-2 bg-[#DDE5B6] text-[#555B4F] font-semibold rounded hover:bg-[#9aa089] cursor-pointer"
                    >
                    OK
                    </button>
                    
                </div>
            </div>
            )}

        </div>

    )

    }
    
}