import React from 'react';
import { useRouter } from 'next/router';
import { Button } from '@chakra-ui/react'


const HomePage = () => {
    const router = useRouter();

    const handleLogin = () => {
        router.push('/login');
    };

    return (
        <div className="flex flex-col min-h-screen bg-gray-100">
            <div className="flex justify-end p-4">
                <div className="ml-auto">
                    <Button onClick={handleLogin} variant={"outline"} colorScheme="telegram" className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                        Login
                    </Button>
                </div>
            </div>
            <div className=" p-6 ml-12 flex items-center justify-start flex-grow">
                <div className="ml-12 max-w-md w-full p-6 bg-white rounded shadow-lg">
                    <div className="flex items-center justify-start">
                        <img src="/logo.png" alt="Icon" width={75} height={75} />
                        <h1 className="text-3xl font-bold mb-2 ml-10">MoneyMate</h1>
                    </div>
                    <p className="text-xl text-gray-600 mb-8 mt-5">Track your expenses effortlessly with our Telegram bot. No need to install any app, All you need is Telegram</p>
                    <p className="text-xl text-gray-600 mb-8">To begin, add @MoneyMate_ExpenseBot to your Telegram group</p>
                    <div className="flex justify-center">
                        <a
                            href="https://t.me/MoneyMate_ExpenseBot"
                            target="_blank"
                            rel="noopener noreferrer"
                            className="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded">
                            Open in Telegram
                        </a>
                    </div>
                </div>
                <div className="flex-grow flex items-center justify-center">
                    <video className="rounded-md shadow-xl" width={350} height={"auto"} autoPlay loop muted>
                        <source src="/vid.mp4" type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                </div>
            </div>
        </div>
    );
};

export default HomePage;
