import React, { useEffect, useState } from "react";
import { ActivityIndicator, FlatList, StyleSheet, Text, View } from "react-native";

const UserTable = () => {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://10.0.2.2:5000/users",{method:"GET"}) // same API as your Flask
      .then((res) => res.json())
      .then((data) => {
        setUsers(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="blue" />
      </View>
    );
  }

  const renderItem = ({ item }) => (
    <View style={styles.row}>
      <Text style={[styles.cell, { flex: 1 }]}>{item.id}</Text>
      <Text style={[styles.cell, { flex: 2 }]}>{item.name}</Text>
      <Text style={[styles.cell, { flex: 1 }]}>Age: {item.age}</Text>
    </View>
  );

  return (
    <View style={styles.container}>
      {/* Header Row */}
      <View style={[styles.row, styles.header]}>
        <Text style={[styles.cell, { flex: 1 }]}>ID</Text>
        <Text style={[styles.cell, { flex: 2 }]}>Name</Text>
        <Text style={[styles.cell, { flex: 1 }]}>Age</Text>
      </View>

      {/* Data Rows */}
      <FlatList
        data={users}
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderItem}
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    paddingTop: 20,
    paddingHorizontal: 15, // left & right
    paddingBottom: 10,
  },
  center: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  row: {
    flexDirection: "row",
    borderBottomWidth: 1,
    borderColor: "#ccc",
    paddingVertical: 8,
  },
  cell: {
    paddingHorizontal: 5,
  },
  header: {
    backgroundColor: "#eee",
    borderBottomWidth: 2,
  },
});

export default UserTable;
