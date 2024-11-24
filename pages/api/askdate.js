export default async function handler(req, res) {
    if (req.method === 'POST') {
      const { date } = req.body;
  
      const backendRes = await fetch('http://localhost:5000/ask', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ date }),
      });
  
      const data = await backendRes.json();
      res.status(200).json(data);
    } else {
      res.status(405).json({ message: 'Method Not Allowed' });
    }
  }
  