import { supabase } from './src/lib/supabase';

async function checkDatabase() {
  try {
    console.log('Checking for user_scans table...');

    const { data, error } = await supabase
      .from('user_scans')
      .select('*')
      .limit(1);

    if (error) {
      console.error('❌ Table does not exist or error occurred:', error.message);
      console.error('Full error:', error);
      return false;
    }

    console.log('✅ Table exists!');
    console.log('Sample data:', data);
    return true;
  } catch (err: any) {
    console.error('❌ Error:', err.message);
    return false;
  }
}

checkDatabase();
