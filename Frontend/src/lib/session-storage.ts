
export const getFromStorage = function(key:string){
    if(typeof window === 'undefined'){
        return
    }
    const data =  sessionStorage.getItem(key)
    if(!data) return 
    return JSON.parse(data)
}

export const setSessionStorage = function(key:string,value:any){
    return sessionStorage.setItem(key,JSON.stringify(value))
}

export const clearFromSession = function(key:string){
    sessionStorage.removeItem(key)
}