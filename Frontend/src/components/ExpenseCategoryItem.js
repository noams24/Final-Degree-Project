import { currencyFormatter } from "@/lib/utils";

function ExpenseCategoryItem({ color, title, total,user, date }) {
  return (
    <button>
<div className="bg-white shadow-md p-2 rounded-lg">   
<div className="flex justify-between">
<div className="flex space-x-3">
        <div className="w-[25px] h-[25px] rounded-full" style={{ backgroundColor: color }}/>
        <div className="text-gray-800 text-xl">{title}</div>
        </div>
        <p>{currencyFormatter(total)}</p>
        </div>
      <div className="flex space-x-7 ml-10">
      <div className="text-gray-400 text-sm">{date}</div>
      <div className="text-gray-400 text-sm">{user}</div>
      </div>
      
    </div>
    </button>
  );
}

export default ExpenseCategoryItem;