export default function Trust() {
  const user = JSON.parse(localStorage.getItem("user"));

  return (
    <div className="min-h-screen flex justify-center items-center bg-gradient-to-r from-purple-600 to-blue-500">

      <div className="bg-white p-8 rounded-2xl shadow-lg w-80 text-center">

        <h2 className="text-xl font-bold mb-4">Trust Score</h2>

        <p className="text-4xl font-bold text-green-600">
          {user?.trust_score}
        </p>

      </div>
    </div>
  );
}